from googlesearch import search

def searchsploit(service, htmlRender=False):
    query = service + " exploit vuln"
    res = search(query, num=10, stop=10, pause=2)

    displayInfos = ""

    if htmlRender:
        spacing = "<br>"
    else:
        spacing = "\n"

    links = []
    for l in res:
        links.append(l)

    if not htmlRender:
        displayInfos += f"\n\n===================================\n"
        displayInfos += f" Exploits concernant " + service
        displayInfos += f"\n===================================\n\n"

    for link in links:
        displayInfos += f"{link}{spacing}"

    return displayInfos

def scan_for_cves(target):
    results = searchsploit(target)
    print(results)

if __name__ == "__main__":
    target = input("Please enter the target IP address or domain to scan for exploitable CVEs: ")
    scan_for_cves(target)
