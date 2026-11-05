# -*- coding: utf-8 -*-
"""
从 OpenAlex 抓取结果生成 data/papers.json。
只需在需要重新同步论文时运行一次：python build_papers.py
"""
import json
import os
import re
import unicodedata
import urllib.request

SRC = "oa_works.json"
OUT = "data/papers.json"
AUTHOR_ID = "A5063699066"          # OpenAlex id for Bolun Zheng @ HDU
MAILTO = "bolunzheng@hdu.edu.cn"
ME = "Bolun Zheng"


def fetch_works():
    """从 OpenAlex 拉取该作者全部作品；已存在 oa_works.json 时复用。"""
    if os.path.exists(SRC):
        return json.load(open(SRC, encoding="utf-8"))

    works, cursor = [], "*"
    while cursor:
        url = ("https://api.openalex.org/works?filter=author.id:%s"
               "&per_page=200&cursor=%s&mailto=%s" % (AUTHOR_ID, cursor, MAILTO))
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.load(urllib.request.urlopen(req, timeout=60))
        works += data["results"]
        cursor = data["meta"].get("next_cursor")
        if not data["results"]:
            break
    json.dump(works, open(SRC, "w", encoding="utf-8"), ensure_ascii=False)
    return works

# 预印本 -> 已发表版本的标题映射（按归一化 key 合并，保留正式版）
DEDUP = {
    "hierarchicalfrequencybasedupsamplingandrefiningforcompressedvideoqualityenhancement":
        "hierarchicalfrequencybasedupsamplingandrefiningforhevc compressedvideoenhancement",
    "wxsodabenchmarkforrobustsalientobjectdetectioninadverseweatherconditions":
        "abenchmarkforrobustsalientobjectdetectioninadverseweatherconditions",
}

VENUE = {
    "IEEE Transactions on Pattern Analysis and Machine Intelligence": ("IEEE TPAMI", "IEEE Transactions on Pattern Analysis and Machine Intelligence"),
    "IEEE Transactions on Image Processing": ("IEEE TIP", "IEEE Transactions on Image Processing"),
    "IEEE Transactions on Circuits and Systems for Video Technology": ("IEEE TCSVT", "IEEE Transactions on Circuits and Systems for Video Technology"),
    "IEEE Transactions on Multimedia": ("IEEE TMM", "IEEE Transactions on Multimedia"),
    "IEEE Transactions on Cybernetics": ("IEEE TCyb", "IEEE Transactions on Cybernetics"),
    "IEEE Transactions on Instrumentation and Measurement": ("IEEE TIM", "IEEE Transactions on Instrumentation and Measurement"),
    "IEEE Transactions on Geoscience and Remote Sensing": ("IEEE TGRS", "IEEE Transactions on Geoscience and Remote Sensing"),
    "IEEE Transactions on Information Forensics and Security": ("IEEE TIFS", "IEEE Transactions on Information Forensics and Security"),
    "IEEE Transactions on Computational Imaging": ("IEEE TCI", "IEEE Transactions on Computational Imaging"),
    "International Journal of Computer Vision": ("IJCV", "International Journal of Computer Vision"),
    "ACM Transactions on Multimedia Computing Communications and Applications": ("ACM TOMM", "ACM Transactions on Multimedia Computing, Communications, and Applications"),
    "ACM Transactions on the Web": ("ACM TWEB", "ACM Transactions on the Web"),
    "IEEE Computer Society Conference on Computer Vision and Pattern Recognition/Proceedings - IEEE Computer Society Conference on Computer Vision and Pattern Recognition/Proceedings": ("CVPR", "IEEE/CVF Conference on Computer Vision and Pattern Recognition"),
    "IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)": ("CVPRW", "IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops"),
    "IEEE International Conference on Computer Vision Workshops": ("ICCVW", "IEEE/CVF International Conference on Computer Vision Workshops"),
    "ACM International Conference on Multimedia (ACM MM)": ("ACM MM", "ACM International Conference on Multimedia"),
    "Proceedings of the AAAI Conference on Artificial Intelligence": ("AAAI", "AAAI Conference on Artificial Intelligence"),
    "IEEE International Conference on Multimedia and Expo (ICME)": ("ICME", "IEEE International Conference on Multimedia and Expo"),
    "IEEE International Conference on Signal, Information and Data Processing (ICSIDP)": ("ICSIDP", "IEEE International Conference on Signal, Information and Data Processing"),
    "Computer Vision and Image Understanding": ("CVIU", "Computer Vision and Image Understanding"),
    "Journal of Visual Communication and Image Representation": ("JVCIR", "Journal of Visual Communication and Image Representation"),
    "Journal of Electronic Imaging": ("JEI", "Journal of Electronic Imaging"),
    "Pattern Recognition": ("Pattern Recognition", "Pattern Recognition"),
    "Pattern Recognition Letters": ("PRL", "Pattern Recognition Letters"),
    "Neural Networks": ("Neural Networks", "Neural Networks"),
    "Neurocomputing": ("Neurocomputing", "Neurocomputing"),
    "IEEE Geoscience and Remote Sensing Letters": ("IEEE GRSL", "IEEE Geoscience and Remote Sensing Letters"),
    "Expert Systems with Applications": ("ESWA", "Expert Systems with Applications"),
    "Applied Soft Computing": ("ASOC", "Applied Soft Computing"),
    "Applied Intelligence": ("Applied Intelligence", "Applied Intelligence"),
    "Neural Computing and Applications": ("NCAA", "Neural Computing and Applications"),
    "Neural Processing Letters": ("NPL", "Neural Processing Letters"),
    "International Journal of Intelligent Systems": ("IJIS", "International Journal of Intelligent Systems"),
    "Multimedia Systems": ("Multimedia Systems", "Multimedia Systems"),
    "Visual Informatics": ("Visual Informatics", "Visual Informatics"),
    "Intelligent Computing": ("Intelligent Computing", "Intelligent Computing"),
    "IEEE Access": ("IEEE Access", "IEEE Access"),
    "Sensors": ("Sensors", "Sensors"),
    "Electronics": ("Electronics", "Electronics"),
    "Scientific Reports": ("Sci. Rep.", "Scientific Reports"),
    "Frontiers in Digital Health": ("Front. Digit. Health", "Frontiers in Digital Health"),
    "Journal of Translational Internal Medicine": ("J. Transl. Intern. Med.", "Journal of Translational Internal Medicine"),
    "ENGINEERING Information Technology & Electronic Engineering": ("FITEE", "Frontiers of Information Technology & Electronic Engineering"),
    "Journal of Computer-Aided Design & Computer Graphics": ("J. Comput.-Aided Des. Comput. Graph.", "Journal of Computer-Aided Design & Computer Graphics"),
    "Journal of Physics Conference Series": ("J. Phys. Conf. Ser.", "Journal of Physics: Conference Series"),
    "arXiv (Cornell University)": ("arXiv", "arXiv preprint"),
    "SSRN Electronic Journal": ("SSRN", "SSRN preprint"),
}

# 代表性论文（手选 14 篇，列表顺序即首页展示顺序：由新到旧）
# 顺序 = 首页 Selected Publications 的排列顺序，改这里就能改顺序
SELECTED = [
    "perceptualqualityassessmentofrealworldnoiseinultrahighdefinitionimages",
    "guidedldrgenerationforsingleimagehdrreconstructionusingexposurepriorsfrommultiexposureimages",
    "learningscenepriorsfromsatelliteimageryforuavimagemotiondeblurring",
    "videodemoireingwithspatialtemporalfilteringinfrequencydomain",
    "ehpeasegmentedarchitectureforenhancedhandposeestimation",
    "smtpd:anewbenchmarkfortemporalpredictionofsocialmediapopularity",
    "pyramidlearnablebandpassfiltersforultrahighdefinitionimagedemoireing",
    "quadbayerjointdemosaicinganddenoisingbasedondualencodernetwork",
    "improvingdynamichdrimagingwithfusiontransformer",
    "domainpluscrosstransformdomainlearningtowardshighdynamicrangeimaging",
    "cbren:convolutionalneuralnetworksforconstantbitratevideoqualityenhancement",
    "learningfrequencydomainpriorsforimagedemoireing",
    "imagedemoireingwithlearnablebandpassfilters",
    "implicitdualdomainconvolutionalnetworkforrobustcolorimagecompressionartifactreduction",
]

# 开源代码 / 项目主页（按归一化标题前缀匹配）
PROJECTS = {
    "guidedldrgenerationforsingleimagehdrreconstructionusingexposurepriorsfrommultiexposureimages": "https://github.com/gguoshun/DG-SHDR",
    "perceptualqualityassessmentofrealworldnoiseinultrahighdefinitionimages": "https://github.com/zijieweng123/PINE",
    "smtpd:anewbenchmarkfortemporalpredictionofsocialmediapopularity": "https://github.com/zhuwei321/SMTPD",
    "quadbayerjointdemosaicinganddenoisingbasedondualencodernetwork": "https://github.com/HrLi97/Aaai2024_DRNet",
    "domainpluscrosstransformdomainlearningtowardshighdynamicrangeimaging": "https://github.com/Pan-xiaokai/DomainPlus-Network",
    "imagedemoireingwithlearnablebandpassfilters": "https://github.com/zhenngbolun/Learnbale_Bandpass_Filter",
    "learningfrequencydomainpriorsforimagedemoireing": "https://github.com/zhenngbolun/Learnbale_Bandpass_Filter",
    "implicitdualdomainconvolutionalnetworkforrobustcolorimagecompressionartifactreduction": "https://github.com/zhenngbolun/IDCN",
}

def norm(s):
    """归一化：é 之类的重音字母先分解成基本字母再保留，避免 Demoiréing -> demoiring。"""
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"[^a-z0-9]", "", s.lower())


SELKEYS = [norm(s) for s in SELECTED]


def sel_rank(k):
    """返回 1-based 顺序号；不在精选列表中返回 0。"""
    for i, s in enumerate(SELKEYS, 1):
        if k.startswith(s):
            return i
    return 0


def project_of(k):
    for s, url in PROJECTS.items():
        if k.startswith(norm(s)):
            return url
    return ""

# OpenAlex 标题里已知的拼写/排版错误
TITLE_FIX = [
    ("Multi-Feature Fusionand Decomposition", "Multi-Feature Fusion and Decomposition"),
    ("S 5 Net", "S5Net"),
    ("Global--Local", "Global–Local"),
    ("bare\u2011bone", "bare-bone"),
]


def fix_title(t):
    for a, b in TITLE_FIX:
        t = t.replace(a, b)
    return t


def key(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def main():
    raw = fetch_works()

    by_key = {}
    for x in raw:
        k = key(x.get("title"))
        if not k:
            continue
        prev = by_key.get(k)
        # 同标题保留引用数更高的那条
        if prev is None or (x.get("cited_by_count") or 0) > (prev.get("cited_by_count") or 0):
            by_key[k] = x

    # 删掉有正式版的预印本
    for pre, pub in DEDUP.items():
        if pre in by_key and pub.replace(" ", "") in by_key:
            del by_key[pre]

    papers = []
    for k, x in by_key.items():
        src = ((x.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        short, full = VENUE.get(src, (src or "Preprint", src or "Preprint"))
        authors = [a["author"]["display_name"] for a in x.get("authorships", [])]
        if ME not in authors:
            continue
        t = x.get("type") or "article"
        kind = "conference" if "conference" in t else ("preprint" if "preprint" in t else "journal")
        doi = (x.get("doi") or "").replace("https://doi.org/", "")
        tn = norm(fix_title((x.get("title") or "").strip().rstrip(".")))
        papers.append({
            "title": fix_title((x.get("title") or "").strip().rstrip(".")),
            "authors": authors,
            "venue": short,
            "venue_full": full,
            "year": x.get("publication_year") or 0,
            "type": kind,
            "doi": doi,
            "url": "https://doi.org/" + doi if doi else "",
            "cites": x.get("cited_by_count") or 0,
            "selected": sel_rank(tn) > 0,
            "rank": sel_rank(tn),
            "project": project_of(tn),
        })

    papers.sort(key=lambda p: (-p["year"], -p["cites"], p["title"]))
    json.dump(papers, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    sel = sum(1 for p in papers if p["selected"])
    years = sorted({p["year"] for p in papers if p["year"]})
    print(f"total={len(papers)}  selected={sel}  years={years[0]}-{years[-1]}")
    for p in papers:
        if p["selected"]:
            print("  *", p["year"], p["venue"], "|", p["title"][:70])


if __name__ == "__main__":
    main()
