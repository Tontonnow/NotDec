#!/usr/bin/python3
import os,sys,re

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
parent_dir = os.path.dirname(script_dir)
# sys.path.insert(1, parent_dir)

type_map = {
    "unsigned": "unsigned long",
    "vid": "unsigned long",
    "tid": "unsigned long",
    "symbol": "std::string",
}

with open(f"{script_dir}/rules/external.dl", "r") as f:
    external = f.readlines()

facts = []
fact_defs = []

for line in external:
    line = line.strip()
    if not line.startswith(".decl"): continue
    # decl, decl_ty = re.match(r".decl\s+(\w+)\s*\(\s*((\w+\s*:\s*\w+[,\s]*)*)\)", line).groups()
    # decl_ty = decl_ty.split(",")
    # decl_ty = [x.strip().split(":") for x in decl_ty]
    # for name, ty in decl_ty:
    #     name = name.strip()
    #     ty = type_map[ty.strip()]
    # print(f"std::map<{decl_ty[0][1]}> {decl}({decl_ty[0][1]});")
    decl = re.search(r".decl\s+(\w+)\s*\(", line).group(1)
    fact_defs.append(f'const char* FACT_{decl} = "{decl}";')
    facts.append(f'extern const char* FACT_{decl};')

with open(f"{script_dir}/fact-names.h", "w") as f:
    f.write('namespace notdec::datalog {\n')
    f.write('\n'.join(facts))
    f.write('\n} // namespace notdec::datalog')

with open(f"{script_dir}/fact-names.def", "w") as f:
    f.write('namespace notdec::datalog {\n')
    f.write('\n'.join(fact_defs))
    f.write('\n} // namespace notdec::datalog')
