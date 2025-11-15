#!/usr/bin/env python3
# universal_factory.py —— 换赛道只改 fetch_mine()
import os, random, requests, itertools, time, multiprocessing as mp
import os, requests, json

###############################################################################
# 1) 只改这里：换赛道 → 换矿场函数
###############################################################################
def fetch_mine():
    # === S1 男频爽文 ===
    repo = random.choice([
        "https://raw.githubusercontent.com/kingyue male-web-novel-templates/main/sample.md",
        "https://raw.githubusercontent.com/power-fantasy/samples/main/chapter.md"
    ])
    try:
        raw = requests.get(repo, timeout=10).text
    except:
        raw = "Title: 重生之我在工厂打螺丝\nHook: 一秒无敌\nCliff: 下一秒被开除"
    return raw[:800]

###############################################################################
# 2) 交付工厂：每条赛道 3 套 SKU
###############################################################################
def sku_a(raw: str) -> str:
    lines = raw.splitlines()
    title = lines[0] if lines else "Title"
    hook  = lines[1] if len(lines) > 1 else "Hook"
    cliff = lines[-1] if lines else "Cliff"
    return f"# {title}\n## Hook\n{hook}\n## Cliff\n{cliff}"

def sku_b(raw: str) -> str:
    lines = raw.splitlines()[:4]
    return "\n".join([f"Chapter {i+1}: {line}" for i, line in enumerate(lines)])

def sku_c(raw: str) -> str:
    return f"Tags: 爽文,穿越,金手指,打脸,{len(raw)}字"

SKU_FUNCS = [sku_a, sku_b, sku_c]

###############################################################################
# 3) 并发层：1 进程 1 SKU，CPU 吃满
###############################################################################
def worker(sku_func, queue):
    for raw in iter(queue.get, None):
        out = sku_func(raw)
        # 这里推 Gumroad / Twitter / Fiverr
        print("[交付完成]", sku_func.__name__, len(out))
        # TODO: 调用 Gumroad API 上架
        # TODO: 调用 Twitter API 发帖

def infinite_feed():
    for _ in itertools.count():
        yield fetch_mine()
        time.sleep(0.5)

###############################################################################
# 4) 一键启动：换赛道只改 fetch_mine()
###############################################################################
if __name__ == "__main__":
    queues = [mp.Queue(maxsize=8) for _ in SKU_FUNCS]
    for q in queues:  # 预填充
        for _ in range(8):
            q.put(next(infinite_feed()))

    # 启动 3 个worker进程
    for i, q in enumerate(queues):
        mp.Process(target=worker, args=(SKU_FUNCS[i], q), daemon=True).start()

    # 后台补货
    def refill():
        for q in itertools.cycle(queues):
            q.put(next(infinite_feed()))
            time.sleep(0.5)

    mp.Process(target=refill, daemon=True).start()

    # 主进程阻塞，保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("【工厂停机】")
