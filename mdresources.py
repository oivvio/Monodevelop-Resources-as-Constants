import os
import jinja2
import argparse
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--csproj', help="full path to .csproj file ", required=True)
parser.add_argument('-n', '--namespace', help="the namespace you want your constants in, if you don't set it it will be deduced from csproj")
parser.add_argument('-r', '--resources', help="The name of the class we put all the resources in", default="Resources")
parser.add_argument('-o', '--output', help="Basename of the output .cs file", required=True)


args = parser.parse_args()
args.projectfolder = os.path.dirname(args.csproj)

args.outputpath = os.path.join(args.projectfolder, args.output)


if not args.namespace:
    args.namespace = os.path.basename(args.projectfolder)

mdresourcespath = os.path.dirname(__file__)

templatesloader = jinja2.FileSystemLoader(mdresourcespath)
env = jinja2.Environment(loader=templatesloader)
template = env.get_template("cstemplate.jinja2")



class Resource:
    def __init__(self, path): 
        self.name = path.replace("\\", "_")
        self.name = self.name.replace(".", "_")
        self.name = self.name.replace("-", "_")

        self.path = path.replace("\\", "/")

members = []
parser = etree.XMLParser()
doc = etree.parse(open(args.csproj))
project =  doc.xpath("//*[local-name()='Project']//*[local-name()='ItemGroup']//*[local-name()='Content']")

for element in project:
    path = element.values()[0]
    if path.find("%40") == -1 and not path.startswith("build"):
        members.append(Resource(path))

output = template.render(namespace=args.namespace, classname=args.resources, members=members)

fh = open(args.outputpath, "w")
fh.write(output)


