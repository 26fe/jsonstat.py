import os
import re
import pprint
import pkg_resources


def parse_requirements(requirement_filename):
    requirements = []
    new_lines = []
    with open(requirement_filename) as f:
        for line in f:

            line = line.strip()

            # skip comments or empty lines
            if re.match(r'(\s*#)|(\s*$)', line):
                new_lines.append(line)
                continue

            if re.match(r'\s*-e\s+', line):
                requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
                new_lines.append(line)
                continue

            if re.match(r'\s*-f\s+', line):
                new_lines.append(line)
                continue

            m = re.search(r'([^\s]*)(==|~=)([\d.]+)', line)
            if m is not None:
                pkg_name = m.group(1)
                pkg_version = pkg_resources.get_distribution(pkg_name).version
                new_line = "{}~={}".format(pkg_name, pkg_version)
                requirements.append(new_line)
                new_lines.append(new_line)
                continue

            requirements.append(line)
            new_lines.append(line)

    return requirements, new_lines


def pin_requirements(requirement_filename):
    pp = pprint.PrettyPrinter(indent=4)
    requirements, new_lines = parse_requirements(requirement_filename)
    pp.pprint(requirements)
    with open(requirement_filename, "w") as f:
        for l in new_lines:
            print(l, file=f)


if __name__ == "__main__":
    requirement_filename = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
    pin_requirements(requirement_filename)
    requirement_filename = os.path.join(os.path.dirname(__file__), "..", "requirements_for_test.txt")
    pin_requirements(requirement_filename)
