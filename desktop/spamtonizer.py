import random
import re
import tkinter as tk
from tkinter import ttk

# --- Spamton speak generator ---

def _is_chinese(text):
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    latin = re.findall(r"[A-Za-z]", text)
    return len(cjk) >= 1 and len(cjk) >= len(latin)

# ============ ENGLISH ============
BRACKET_WORDS = [
    "BIG SHOT", "HYPERLINK BLOCKED", "LINK", "DEAL", "BROTHER", "FRIEND",
    "FREEDOM", "SPECIAL", "OFFER", "PROMOTION", "[DEAL]", "VIP",
    "SALE", "SALESMAN", "PATHS", "WORLD", "PAIN", "[BIG SHOT]",
    "HELP", "FUNNY", "PIPE", "[LINK]", "DISCOUNT", "the real deal",
]

INTERJECTIONS = [
    "HEY EVERY!!",
    "IT'S ME!!",
    "WOW!!!",
    "WHY?!",
    "WHAT THE!!",
    "YOU!!!",
    "LISTEN!!",
    "PLEASE!",
    "CONGRATULATIONS!!!",
    "WAIT!!!",
    "OH NO!!",
    "... eh?",
]

REGARDS = [
    "real", "true", "genuine", "PEOPLE", "friend", "salesman",
    "champion", "special friend", "[the real deal]",
]

END_FILLERS = [
    "HELP!!!", "PLEASE!!!", "SHOW ME THE [LINK]!!!", 
    "GIMME THAT [BIG SHOT]!!!", "ITS MY [SPECIAL]!!",
    "YOU DON'T GET IT??? ... THAT'S RIGHT, YOU DO!!!",
    "HEE HEE! HOO HOO!! ... AHAHAHAHA!!!",
    "THE PRICE?? ... [EVERYTHING]!!",
    "SO [SPECIAL]!! WANNA MAKE A [DEAL]??",
    "WANNA BE FREE?? [BROTHER]!!",
]

PRICES = [
    "99.95", "199.99", "115.5", "79.99", "FREE",
    "00.00", "[FREE]", "99.30", "27", "10", "2002",
]

# ============ CHINESE ============
CN_BRACKET = [
    "链接", "优惠", "自由", "真正的交易", "合作", "兄弟", "朋友",
    "超值", "促销", "特别", "一折", "好价", "批发", "赚翻了",
    "大酬宾", "清仓", "VIP", "准链接", "暴利",
]

CN_INTERJ = [
    "HEY!!大家都!!",
    "IT'S ME!!!",
    "是我!!!",
    "哇!!!!",
    "为什么?!?!",
    "你!!!",
    "听我说!!!",
    "拜托!!!",
    "恭喜!!!!",
    "等等!!!",
    "噢不!!",
    "呵呵呵!!",
]

CN_REGARDS = [
    "真的", "真正的", "可信的", "朋友", "兄弟", "合伙人",
    "大客户", "专属贵宾", "天生的销售", "老实人",
]

CN_END = [
    "救救我!!!",
    "拜托了!!!",
    "快把那个[[链接]]给我!!!",
    "快给我[[优惠]]!!",
    "这[[价格]]我可不能改!!",
    "嘿嘿嘿!!呵呵呵!!哈哈哈哈!!!",
    "你想变得[[自由]]吗??兄弟!!!",
    "只要付出[[一切]]!!",
    "这就是[[真正的交易]]!!",
    "快把它抢走吧!!",
]

CN_PRICES = [
    "99.95", "199.99", "115.5", "79.99", "免费", "白送",
    "2002", "0.99", "一元", "二十", "八八", "三折", "统统免费",
]

CN_PUNCT = [".", "...", "!", "!!", "?", "?", "~", "~"]

def spamtonize_cn(text, intensity=1.0, filler=True, price=True):
    rng = random.Random()
    raw = re.sub(r"\s+", "", text).strip()
    if not raw:
        return ""
    out_parts = []
    words = re.findall(r"[A-Za-z0-9']+|[.,!?。，！？；：、…<>]|.", raw)
    built = []
    idx = 0
    used_cn = set()
    used_p = set()
    for w in words:
        if not w or w in " \t":
            continue
        if re.fullmatch(r"[.,;!?。，！？；：、…]", w):
            built.append(w)
            continue
        cur = w
        if price and rng.random() < 0.07 * intensity:
            cur = rng.choice([x for x in CN_PRICES if x not in used_p] or CN_PRICES)
            used_p.add(cur)
        if rng.random() < 0.06 * intensity:
            cur = cur + rng.choice(["!", "?", "...", "."])
        # random character repetition for emphasis
        if rng.random() < 0.03 * intensity and len(cur) == 1 and re.match(r"[\u4e00-\u9fff]", cur):
            cur = cur * rng.randint(2, 2)
        if rng.random() < 0.06 * intensity:
            pick = rng.choice([b for b in CN_BRACKET if b not in used_cn] or CN_BRACKET)
            used_cn.add(pick)
            built.append("[[" + pick + "]]")
        built.append(cur)
        idx += 1
        if idx % 6 == 0 and rng.random() < 0.14 * intensity:
            built.append(rng.choice(CN_PUNCT))
    joined = re.sub(r"\s+", "", "".join(built))
    out_parts.append(joined)
    final = "".join(out_parts)
    if filler:
        n = rng.randint(0, max(0, int(2 * intensity) - 1))
        picks = rng.sample(CN_INTERJ, k=min(n, len(CN_INTERJ)))
        for p in picks:
            final = p + " " + final
        if rng.random() < 0.55 * intensity:
            final = final + " " + rng.choice(CN_END)
    final = re.sub(r"\s+", " ", final).strip()
    return final

def _capify(word, rng):
    mode = rng.random()
    if mode < 0.45:
        return word.upper()
    if mode < 0.55:
        return word.capitalize()
    if mode < 0.62 and len(word) > 2:
        chars = list(word)
        for i in range(len(chars)):
            if chars[i].isalpha() and rng.random() < 0.5:
                chars[i] = chars[i].upper()
        return "".join(chars)
    return word

def _maybe_bracket(word, rng, intensity):
    if rng.random() < 0.15 * intensity:
        pick = rng.choice(BRACKET_WORDS)
        return f" [[{pick}] ]"
    return word

def _punct(rng):
    r = rng.random()
    if r < 0.3:
        return "..."
    if r < 0.55:
        return "."
    if r < 0.75:
        return "!"
    if r < 0.9:
        return "?"
    return "~"

def spamtonize(text, intensity=1.0, filler=True, price=True):
    raw = re.sub(r"\s+", " ", text).strip()
    if not raw:
        return ""
    if _is_chinese(raw):
        return spamtonize_cn(raw, intensity=intensity, filler=filler, price=price)
    rng = random.Random()
    sentences = re.findall(r"[^.!?]+[.!?]*", raw) or [raw]
    out_parts = []

    i = 0
    used_cn = set()
    used_p = set()
    for sent in sentences:
        words = re.findall(r"[\w'-]+|[^\w\s]", sent)
        new_words = []
        for w in words:
            if not re.search(r"[\w]", w):
                new_words.append(w)
                continue
            cw = _capify(w, rng)
            if price and rng.random() < 0.06 * intensity:
                cw = rng.choice([x for x in PRICES if x not in used_p] or PRICES)
                used_p.add(cw)
            if rng.random() < 0.05 * intensity:
                cw = cw.upper() + " " + rng.choice(REGARDS).upper()
            if rng.random() < 0.1 * intensity:
                pick = rng.choice([b for b in BRACKET_WORDS if b not in used_cn] or BRACKET_WORDS)
                used_cn.add(pick)
                new_words.append(pick if "[" in pick else "[[" + pick + "]]")
                i += 1
            new_words.append(cw)
            i += 1
            if i % 6 == 0 and rng.random() < 0.18 * intensity:
                new_words.append(_punct(rng))
        joined = " ".join(new_words)
        joined = joined.rstrip(". ").rstrip()
        out_parts.append(joined + rng.choice([".", "...", "!", "?", "?", "...", "!"]))

    final = " ".join(out_parts)

    if filler:
        # sprinkle a few distinct interjections
        n = rng.randint(0, max(0, int(2 * intensity) - 1))
        picks = rng.sample(INTERJECTIONS, k=min(n, len(INTERJECTIONS)))
        for p in picks:
            final = p + " " + final
        if rng.random() < 0.5 * intensity:
            final = final + " " + rng.choice(END_FILLERS)

    final = re.sub(r"\s+([,.;:!?])", r"\1", final)
    final = re.sub(r" {2,}", " ", final).strip()
    return final


# --- GUI ---

class App:
    def __init__(self, root):
        root.title("SPAMTONIZER !! [BIG SHOT] edition")
        root.geometry("640x560")
        root.minsize(520, 460)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        root.configure(bg="#1a1a24")

        pad = {"padx": 12, "pady": 8}

        title = tk.Label(root, text="SPAMTON SPEAK CONVERTER !!!",
                         bg="#1a1a24", fg="#ff4dff",
                         font=("Segoe UI", 18, "bold"))
        title.pack(**pad)

        in_lbl = tk.Label(root, text="说点什么 / Type here -> [[LINK]]",
                          bg="#1a1a24", fg="#cccccc", font=("Segoe UI", 10))
        in_lbl.pack(anchor="w", padx=12)

        self.in_text = tk.Text(root, height=6, font=("Consolas", 12),
                               bg="#12121c", fg="#eeeeee",
                               insertbackground="#ffffff", relief="flat")
        self.in_text.pack(fill="x", padx=12)
        self.in_text.insert("1.0", "HEY EVERY!! this is where your words go, friend...")


        opt_frame = tk.Frame(root, bg="#1a1a24")
        opt_frame.pack(fill="x", padx=12, pady=6)

        tk.Label(opt_frame, text="疯狂程度 / SPAM:", bg="#1a1a24", fg="#cccccc").pack(side="left")
        self.intensity = ttk.Combobox(opt_frame, values=["过轻 / mild", "适中 / mid", "疯狂 / MAX"],
                                      state="readonly", width=14)
        self.intensity.current(1)
        self.intensity.pack(side="left", padx=8)

        self.var_filler = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_frame, text="加碎碎念 / filler", variable=self.var_filler).pack(side="left", padx=8)
        self.var_price = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_frame, text="加价格 / price", variable=self.var_price).pack(side="left")

        btns = tk.Frame(root, bg="#1a1a24")
        btns.pack(pady=6)
        ttk.Button(btns, text="转换 !! CONVERT !!", command=self.convert).pack(side="left", padx=6)
        ttk.Button(btns, text="复制 COPY", command=self.copy).pack(side="left", padx=6)

        self.out_text = tk.Text(root, height=9, font=("Consolas", 12),
                                bg="#12121c", fg="#7fff7f",
                                state="disabled", relief="flat", wrap="word")
        self.out_text.pack(fill="both", expand=True, padx=12, pady=8)

        tk.Label(root, text="PRODUCED BY SPAMTON G. SPAMTON - THE merch MAN !!",
                 bg="#1a1a24", fg="#666666", font=("Segoe UI", 8)).pack(pady=(0, 6))

        self.in_text.bind("<Control-Return>", lambda e: self.convert())

    def _intensity(self):
        return {0: 0.5, 1: 1.0, 2: 1.8}[self.intensity.current()]

    def convert(self):
        text = self.in_text.get("1.0", "end")
        result = spamtonize(text,
                            intensity=self._intensity(),
                            filler=self.var_filler.get(),
                            price=self.var_price.get())
        self.out_text.configure(state="normal")
        self.out_text.delete("1.0", "end")
        self.out_text.insert("1.0", result)
        self.out_text.configure(state="disabled")

    def copy(self):
        root.clipboard_clear()
        root.clipboard_append(self.out_text.get("1.0", "end").strip())
        root.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()