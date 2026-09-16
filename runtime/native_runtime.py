#!/usr/bin/env python3
"""
$brush-creator-studio V2.1 native runtime.

Scope:
- Procreate .brush / .brushset structural inspection
- Git LFS pointer detection and best-effort local resolution
- evidence-safe derivation from a valid .brush base
- .brushset assembly from validated .brush files
- family/package validation
- delivery ZIP count-consistency validation

Important:
Structural PACKAGE validation is not equivalent to a real Procreate import/drawing test.
FULL PASS requires target-software validation outside this module.
"""
from __future__ import annotations
import argparse, hashlib, json, os, plistlib, re, shutil, subprocess, tempfile, uuid, zipfile
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple, Union
PathLike = Union[str, os.PathLike]
LFS_HEADER = b"version https://git-lfs.github.com/spec/v1"
LFS_OID_RE = re.compile(rb"oid sha256:([0-9a-f]{64})")
LFS_SIZE_RE = re.compile(rb"size ([0-9]+)")
REQUIRED_BRUSH_MEMBER = "Brush.archive"
SAFE_ARCHIVE_PATCH_FIELDS = {"plotSpacing","plotJitter","plotJitterLongitudinal","plotSmoothing","maxSize","minSize","maxOpacity","minOpacity","dynamicsPressureSize","dynamicsPressureOpacity","dynamicsPressureResponse","dynamicsTiltSize","wetEdgesAmount","dynamicsWetAccumulation","dynamicsWetnessJitter","dynamicsLoad","dynamicsPressureMix","dynamicsSmudgeAccumulation","grainDepth","textureScale","textureContrast","paintSize","paintOpacity","smudgeSize","smudgeOpacity"}
def _result(status: str, *, evidence_state: str="UNVERIFIED", internal_name: Optional[str]=None, sha256: Optional[str]=None, member_count: Optional[int]=None, missing_members: Optional[Sequence[str]]=None, extra_members: Optional[Sequence[str]]=None, errors: Optional[Sequence[str]]=None, **extra: Any)->Dict[str,Any]:
    out={"status":status,"evidence_state":evidence_state,"internal_name":internal_name,"sha256":sha256,"member_count":member_count,"missing_members":list(missing_members or []),"extra_members":list(extra_members or []),"errors":list(errors or [])}; out.update(extra); return out
def _read_bytes(x):
    return bytes(x) if isinstance(x,(bytes,bytearray)) else Path(x).read_bytes()
def _sha256_bytes(data: bytes)->str: return hashlib.sha256(data).hexdigest()
def _sha256_file(path: PathLike)->str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def detect_lfs_pointer(path_or_bytes)->Dict[str,Any]:
    try: data=_read_bytes(path_or_bytes)
    except Exception as exc: return _result("READ_FAILED",errors=[str(exc)])
    head=data[:1024]
    if not head.startswith(LFS_HEADER): return _result("NOT_LFS_POINTER",evidence_state="VERIFIED_METADATA",sha256=_sha256_bytes(data),is_lfs_pointer=False)
    oid=LFS_OID_RE.search(head); size=LFS_SIZE_RE.search(head)
    return _result("LFS_POINTER",evidence_state="VERIFIED_METADATA",sha256=_sha256_bytes(data),is_lfs_pointer=True,lfs_oid_sha256=oid.group(1).decode() if oid else None,lfs_size=int(size.group(1)) if size else None)
def _decode_archive(data: bytes)->Tuple[Dict[str,Any],list,Dict[str,Any]]:
    payload=plistlib.loads(data); objs=payload.get("$objects")
    if not isinstance(objs,list) or len(objs)<2 or not isinstance(objs[1],dict): raise ValueError("Unsupported Brush.archive keyed-archive structure")
    return payload,objs,objs[1]
def _uid_value(objs,value):
    if isinstance(value,plistlib.UID) and 0<=value.data<len(objs): return objs[value.data]
    return value
def _brush_name_from_archive(data: bytes)->Optional[str]:
    try:
        _,objs,root=_decode_archive(data); name=_uid_value(objs,root.get("name")); return name if isinstance(name,str) else None
    except Exception: return None
def _metadata_subset(root):
    keys=["version","plotSpacing","plotJitter","plotJitterLongitudinal","plotSmoothing","maxSize","minSize","maxOpacity","minOpacity","dynamicsPressureSize","dynamicsPressureOpacity","dynamicsPressureResponse","dynamicsTiltSize","wetEdgesAmount","dynamicsWetAccumulation","dynamicsWetnessJitter","dynamicsLoad","dynamicsPressureMix","dynamicsSmudgeAccumulation","grainDepth","textureScale","textureContrast","textureMovement","shapeCount","shapeScatter","shapeRandomise","importedFromABR","renderingRecursiveMixing","paintSize","paintOpacity","smudgeSize","smudgeOpacity"]
    return {k:root[k] for k in keys if k in root and isinstance(root[k],(str,int,float,bool))}
def inspect_brush(file: PathLike)->Dict[str,Any]:
    p=Path(file)
    if not p.exists(): return _result("BRUSH_NOT_FOUND",errors=[str(p)])
    lfs=detect_lfs_pointer(p)
    if lfs.get("is_lfs_pointer"): return _result("BRUSH_LFS_POINTER_BLOCKED",evidence_state="VERIFIED_METADATA",sha256=_sha256_file(p),errors=["Git LFS pointer is not a native .brush package"],lfs=lfs)
    try:
        if not zipfile.is_zipfile(p): return _result("INVALID_BRUSH_STRUCTURE",sha256=_sha256_file(p),errors=[".brush is not a ZIP-based native package"])
        with zipfile.ZipFile(p) as z:
            names=z.namelist()
            if REQUIRED_BRUSH_MEMBER not in names: return _result("INVALID_BRUSH_STRUCTURE",sha256=_sha256_file(p),missing_members=[REQUIRED_BRUSH_MEMBER],errors=["Required Brush.archive missing"])
            archive=z.read(REQUIRED_BRUSH_MEMBER); internal=_brush_name_from_archive(archive)
            try: _,_,root=_decode_archive(archive); metadata=_metadata_subset(root)
            except Exception as exc: return _result("BRUSH_ARCHIVE_UNSUPPORTED",internal_name=internal,sha256=_sha256_file(p),errors=[str(exc)],zip_members=names)
            return _result("PASS",evidence_state="VERIFIED_METADATA",internal_name=internal,sha256=_sha256_file(p),member_count=1,metadata=metadata,zip_members=names,structural_validation="PACKAGE_STRUCTURE_ONLY")
    except Exception as exc: return _result("BRUSH_INSPECTION_FAILED",sha256=_sha256_file(p),errors=[str(exc)])
def inspect_brushset(file: PathLike)->Dict[str,Any]:
    p=Path(file)
    if not p.exists(): return _result("BRUSHSET_NOT_FOUND",errors=[str(p)])
    lfs=detect_lfs_pointer(p)
    if lfs.get("is_lfs_pointer"): return _result("BRUSHSET_LFS_POINTER_BLOCKED",evidence_state="VERIFIED_METADATA",sha256=_sha256_file(p),errors=["Git LFS pointer is not a native .brushset"],lfs=lfs)
    if not zipfile.is_zipfile(p): return _result("INVALID_BRUSHSET_STRUCTURE",sha256=_sha256_file(p),errors=[".brushset is not a ZIP-based native package"])
    try:
        with zipfile.ZipFile(p) as z:
            names=z.namelist()
            if "brushset.plist" not in names: return _result("INVALID_BRUSHSET_STRUCTURE",sha256=_sha256_file(p),missing_members=["brushset.plist"],errors=["brushset.plist missing"])
            pl=plistlib.loads(z.read("brushset.plist")); order=pl.get("brushes",[]) if isinstance(pl,dict) else []; set_name=pl.get("name") if isinstance(pl,dict) else None
            if not isinstance(order,list): order=[]
            archive_dirs={n.split("/",1)[0] for n in names if n.count("/")==1 and n.endswith("/Brush.archive")}; missing=[m for m in order if m not in archive_dirs]; extra=[m for m in archive_dirs if m not in order]
            members=[]
            for mid in order:
                ap=f"{mid}/Brush.archive"; members.append({"member_id":mid,"internal_name":_brush_name_from_archive(z.read(ap)) if ap in names else None})
            status="PASS" if not missing else "INVALID_BRUSHSET_STRUCTURE"
            return _result(status,evidence_state="VERIFIED_METADATA" if status=="PASS" else "UNVERIFIED",internal_name=set_name,sha256=_sha256_file(p),member_count=len(order),missing_members=missing,extra_members=extra,members=members,declared_order=order,structural_validation="PACKAGE_STRUCTURE_ONLY")
    except Exception as exc: return _result("BRUSHSET_INSPECTION_FAILED",sha256=_sha256_file(p),errors=[str(exc)])
def resolve_lfs_asset(source: PathLike)->Dict[str,Any]:
    p=Path(source)
    if not p.exists(): return _result("LFS_SOURCE_NOT_FOUND",errors=[str(p)])
    state=detect_lfs_pointer(p)
    if not state.get("is_lfs_pointer"): return _result("PASS",evidence_state="VERIFIED_METADATA",sha256=_sha256_file(p),resolved_path=str(p),was_lfs_pointer=False)
    try:
        root=subprocess.run(["git","-C",str(p.parent),"rev-parse","--show-toplevel"],capture_output=True,text=True,check=True).stdout.strip(); rel=os.path.relpath(p.resolve(),Path(root).resolve())
        subprocess.run(["git","-C",root,"lfs","pull","--include",rel,"--exclude",""],capture_output=True,text=True,check=True)
        after=detect_lfs_pointer(p)
        if after.get("is_lfs_pointer"): return _result("LFS_RESOLUTION_BLOCKED",errors=["git lfs pull completed but file is still a pointer"],lfs=after)
        return _result("PASS",evidence_state="VERIFIED_METADATA",sha256=_sha256_file(p),resolved_path=str(p),was_lfs_pointer=True)
    except Exception as exc: return _result("LFS_RESOLUTION_BLOCKED",errors=[str(exc)],lfs=state)
def _rewrite_zip_member(source: Path,output: Path,member: str,replacement: bytes):
    with zipfile.ZipFile(source,"r") as src, zipfile.ZipFile(output,"w") as dst:
        for info in src.infolist():
            data=replacement if info.filename==member else src.read(info.filename); ni=zipfile.ZipInfo(info.filename,date_time=info.date_time); ni.compress_type=info.compress_type; ni.comment=info.comment; ni.extra=info.extra; ni.internal_attr=info.internal_attr; ni.external_attr=info.external_attr; ni.create_system=info.create_system; dst.writestr(ni,data)
def derive_or_build_brush(base: PathLike,spec: Dict[str,Any],output: PathLike)->Dict[str,Any]:
    bp=Path(base); op=Path(output); ins=inspect_brush(bp)
    if ins.get("status")!="PASS": return _result("NATIVE_BUILD_BLOCKED",errors=["Base brush failed native structural inspection"]+ins.get("errors",[]))
    operation=str(spec.get("operation","KEEP")).upper(); op.parent.mkdir(parents=True,exist_ok=True)
    if operation in {"KEEP","COPY"} and not spec.get("metadata_patch") and not spec.get("internal_name"): shutil.copy2(bp,op); out=inspect_brush(op); out["build_operation"]=operation; return out
    if operation not in {"ADJUST","DERIVE","NEW"}: return _result("NATIVE_BUILD_UNSUPPORTED",errors=[f"Unsupported operation: {operation}"])
    if operation=="NEW" and not spec.get("allow_new_from_validated_base"): return _result("NATIVE_BUILD_UNSUPPORTED",errors=["NEW requires an explicitly validated native base or external format-specific builder"])
    try:
        with zipfile.ZipFile(bp) as z: archive=z.read(REQUIRED_BRUSH_MEMBER)
        payload,objs,root=_decode_archive(archive); patch=spec.get("metadata_patch") or {}; unknown=sorted(set(patch)-SAFE_ARCHIVE_PATCH_FIELDS)
        if unknown: return _result("NATIVE_BUILD_UNSUPPORTED",errors=[f"Unsafe/unrecognized Brush.archive patch fields: {unknown}"])
        for k,v in patch.items():
            if not isinstance(v,(int,float,bool,str)): return _result("NATIVE_BUILD_UNSUPPORTED",errors=[f"Non-scalar patch value for {k}"])
            root[k]=v
        name=spec.get("internal_name")
        if name:
            ref=root.get("name")
            if isinstance(ref,plistlib.UID) and 0<=ref.data<len(objs): objs[ref.data]=str(name)
            elif isinstance(ref,str): root["name"]=str(name)
            else: return _result("NATIVE_BUILD_UNSUPPORTED",errors=["Could not safely update internal brush name"])
        rebuilt=plistlib.dumps(payload,fmt=plistlib.FMT_BINARY,sort_keys=False); _rewrite_zip_member(bp,op,REQUIRED_BRUSH_MEMBER,rebuilt); out=inspect_brush(op); out["build_operation"]=operation; out["build_evidence_state"]="PROPOSED"
        if out.get("status")=="PASS": out["status"]="PACKAGE_STRUCTURE_PASS"; out["evidence_state"]="VERIFIED_METADATA"
        return out
    except Exception as exc: return _result("NATIVE_BUILD_FAILED",errors=[str(exc)])
def _unique_member_id()->str: return str(uuid.uuid4()).upper()
def build_brushset(brush_files: Sequence[PathLike],output: PathLike,set_name: str="Brush Creator Studio")->Dict[str,Any]:
    if not brush_files: return _result("NATIVE_BUILD_FAILED",errors=["No brush files supplied"])
    inspections=[inspect_brush(p) for p in brush_files]; failed=[r for r in inspections if r.get("status") not in {"PASS","PACKAGE_STRUCTURE_PASS"}]
    if failed: return _result("NATIVE_BUILD_BLOCKED",errors=["At least one brush failed structural validation"],failed_brushes=failed)
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True); ids=[_unique_member_id() for _ in brush_files]
    try:
        with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as oz:
            oz.writestr("brushset.plist",plistlib.dumps({"brushes":ids,"name":set_name},fmt=plistlib.FMT_XML))
            for brush,mid in zip(brush_files,ids):
                with zipfile.ZipFile(brush) as src:
                    for info in src.infolist():
                        if info.filename.endswith("/") or info.filename.startswith("__MACOSX/"): continue
                        oz.writestr(f"{mid}/{info.filename}",src.read(info.filename))
        checked=inspect_brushset(out); checked["source_brush_names"]=[x.get("internal_name") for x in inspections]; return checked
    except Exception as exc: return _result("NATIVE_BUILD_FAILED",errors=[str(exc)])
def validate_native_family(brushes: Sequence[PathLike],brushset: PathLike)->Dict[str,Any]:
    br=[inspect_brush(p) for p in brushes]; sr=inspect_brushset(brushset); errors=[]
    if any(r.get("status") not in {"PASS","PACKAGE_STRUCTURE_PASS"} for r in br): errors.append("One or more individual .brush files failed structural validation")
    if sr.get("status")!="PASS": errors.append(".brushset failed structural validation")
    bn=[r.get("internal_name") for r in br]; sn=[m.get("internal_name") for m in sr.get("members",[])]; missing=sorted({n for n in bn if n and n not in sn}); extra=sorted({n for n in sn if n and n not in bn})
    if len(br)!=sr.get("member_count"): errors.append("Individual brush count != brushset member count")
    if missing: errors.append("Some delivered brushes are missing from brushset")
    return _result("PASS" if not errors else "FAMILY_VALIDATION_FAILED",evidence_state="VERIFIED_METADATA" if not errors else "UNVERIFIED",member_count=sr.get("member_count"),missing_members=missing,extra_members=extra,errors=errors,individual_brush_count=len(br),brush_names=bn,brushset_names=sn,count_consistent=(len(br)==sr.get("member_count")))
def validate_delivery_zip(zip_path: PathLike,xlsx_reference_list: Optional[Sequence[str]]=None)->Dict[str,Any]:
    p=Path(zip_path)
    if not p.exists() or not zipfile.is_zipfile(p): return _result("DELIVERY_ZIP_INVALID",errors=["ZIP missing or invalid"])
    errors=[]
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(p) as z: z.extractall(td); files=[Path(td)/n for n in z.namelist() if not n.endswith("/")]
        brushes=[f for f in files if f.suffix==".brush"]; sets=[f for f in files if f.suffix==".brushset"]; xlsx=[f for f in files if f.suffix.lower()==".xlsx"]
        if not brushes: errors.append("No .brush files in delivery ZIP")
        if len(sets)!=1: errors.append("Delivery ZIP must contain exactly one .brushset")
        if len(xlsx)!=1: errors.append("Delivery ZIP must contain exactly one project XLSX")
        family=validate_native_family(brushes,sets[0]) if brushes and len(sets)==1 else None
        if family and family.get("status")!="PASS": errors.extend(family.get("errors",[]))
        names=[r.get("internal_name") for r in [inspect_brush(b) for b in brushes] if r.get("internal_name")]; refs=sorted(set(xlsx_reference_list or [])); missing=sorted(set(refs)-set(names)) if refs else []; extra=sorted(set(names)-set(refs)) if refs else []
        if missing: errors.append("XLSX references brushes not present in delivery")
        if family and refs and family.get("member_count")!=len(refs): errors.append("Brushset member count != XLSX referenced distinct brush count")
        return _result("PACKAGE_PASS" if not errors else "PACKAGE_VALIDATION_FAILED",evidence_state="VERIFIED_METADATA" if not errors else "UNVERIFIED",sha256=_sha256_file(p),member_count=family.get("member_count") if family else None,missing_members=missing,extra_members=extra,errors=errors,delivered_brush_count=len(brushes),brushset_count=len(sets),xlsx_count=len(xlsx),xlsx_referenced_distinct_count=len(refs) if refs else None,final_distinct_native_brush_count=len(set(names)),full_pass=False,full_pass_reason="Real Procreate import/drawing test not executed by this structural runtime.")
def _cli()->int:
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("inspect-brush"); p.add_argument("file")
    p=sub.add_parser("inspect-brushset"); p.add_argument("file")
    p=sub.add_parser("detect-lfs"); p.add_argument("file")
    p=sub.add_parser("resolve-lfs"); p.add_argument("file")
    p=sub.add_parser("build-brushset"); p.add_argument("output"); p.add_argument("brushes",nargs="+"); p.add_argument("--name",default="Brush Creator Studio")
    p=sub.add_parser("validate-family"); p.add_argument("brushset"); p.add_argument("brushes",nargs="+")
    p=sub.add_parser("validate-zip"); p.add_argument("zip"); p.add_argument("--refs-json")
    a=ap.parse_args()
    if a.cmd=="inspect-brush": r=inspect_brush(a.file)
    elif a.cmd=="inspect-brushset": r=inspect_brushset(a.file)
    elif a.cmd=="detect-lfs": r=detect_lfs_pointer(a.file)
    elif a.cmd=="resolve-lfs": r=resolve_lfs_asset(a.file)
    elif a.cmd=="build-brushset": r=build_brushset(a.brushes,a.output,a.name)
    elif a.cmd=="validate-family": r=validate_native_family(a.brushes,a.brushset)
    else:
        refs=json.loads(Path(a.refs_json).read_text(encoding="utf-8")) if a.refs_json else None; r=validate_delivery_zip(a.zip,refs)
    print(json.dumps(r,ensure_ascii=False,indent=2,default=str)); return 0 if r.get("status") in {"PASS","PACKAGE_PASS","PACKAGE_STRUCTURE_PASS","NOT_LFS_POINTER"} else 2
if __name__=="__main__": raise SystemExit(_cli())
