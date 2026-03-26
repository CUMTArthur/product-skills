#!/usr/bin/env python3
"""
埋点字典查询工具
快速查询埋点字典中的埋点定义、参数、版本信息等
"""

import pandas as pd
import json
import sys
from pathlib import Path

# 埋点字典路径
DICT_PATH = Path('/Users/arthur/Downloads/埋点字典.xlsx')

# 模块映射表
MODULE_MAP = {
    '目录': 1,
    '修订记录': 2,
    '公共信息': 3,
    '数据': 4,
    '网页端': 5,
    '主页': 6,
    '主页曝光': 7,
    '搜索曝光': 8,
    '赛程列表页': 9,
    '懂球帝': 10,
    '小组件&灵动岛': 11,
    '赛程列表页曝光': 12,
    '推送': 13,
    '新闻': 14,
    '新闻曝光': 15,
    '主队频道': 16,
    '主队曝光': 17,
    '兴趣运动关注': 18,
    '榜单': 19,
    '内页公共': 20,
    '视频': 21,
    '社区': 22,
    '数据曝光': 23,
    '左侧菜单': 24,
    '设置': 25,
    'Apple watch推荐赛程': 26,
    '综合内页': 27,
    '综合内页曝光': 28,
    '装备商城': 29,
    '装备曝光': 30,
    '搜索': 31,
    '登录|注册': 32,
    '评分': 33,
    '评分曝光': 34,
    '评论': 35,
    '评论曝光': 36,
    '专家': 37,
    '准球': 38,
    '钱包、支付': 39,
    '广告': 40,
    '曝光': 41,
    '分享': 42,
    '草稿': 43,
    '游戏': 44,
    '前端': 45,
    '电商直播': 46,
    '日志': 47,
    '赛程日历': 48,
}

def load_sheet(sheet_name):
    """加载指定 sheet"""
    try:
        df = pd.read_excel(DICT_PATH, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"❌ 加载 Sheet '{sheet_name}' 失败: {e}")
        return None

def search_event(keyword, sheet_name=None):
    """搜索埋点事件"""
    results = []
    
    sheets_to_search = [sheet_name] if sheet_name else list(MODULE_MAP.keys())[3:]  # 跳过前3个
    
    for sheet in sheets_to_search:
        df = load_sheet(sheet)
        if df is None:
            continue
        
        # 搜索 event 列
        if 'event' in df.columns:
            matches = df[df['event'].astype(str).str.contains(keyword, na=False)]
            for _, row in matches.iterrows():
                results.append({
                    'sheet': sheet,
                    'model': row.get('model', ''),
                    'event': row.get('event', ''),
                    'type': row.get('type', ''),
                    'params': row.get('params', ''),
                })
    
    return results

def get_module_events(module_name):
    """获取模块的所有埋点"""
    sheet_idx = MODULE_MAP.get(module_name)
    if not sheet_idx:
        return None
    
    df = load_sheet(module_name)
    if df is None:
        return None
    
    events = []
    for _, row in df.iterrows():
        if pd.notna(row.get('event')):
            events.append({
                'model': row.get('model', ''),
                'event': row.get('event', ''),
                'type': row.get('type', ''),
                'params': row.get('params', ''),
                '取值说明': row.get('取值说明', ''),
                '修订记录': row.get('修订记录', ''),
            })
    
    return events

def format_event_json(event):
    """格式化为 JSON"""
    return json.dumps({
        'model': event.get('model', ''),
        'event': event.get('event', ''),
        'type': event.get('type', ''),
        'params': str(event.get('params', '')).split('、') if event.get('params') else [],
        '取值说明': event.get('取值说明', ''),
        '修订记录': event.get('修订记录', ''),
    }, ensure_ascii=False, indent=2)

def print_event(event):
    """打印埋点信息"""
    print(f"\n📍 {event.get('model', 'N/A')} > {event.get('event', 'N/A')}")
    print(f"   Type: {event.get('type', 'N/A')}")
    print(f"   Params: {event.get('params', 'N/A')}")
    if event.get('取值说明'):
        print(f"   说明: {event.get('取值说明', '')}")
    if event.get('修订记录'):
        print(f"   版本: {event.get('修订记录', '')}")

def main():
    if len(sys.argv) < 2:
        print("埋点字典查询工具")
        print("\n用法:")
        print("  python tracking_dict.py list                    # 列出所有模块")
        print("  python tracking_dict.py module <模块名>         # 查询模块的所有埋点")
        print("  python tracking_dict.py search <关键词>         # 搜索埋点")
        print("  python tracking_dict.py search <关键词> <模块>  # 在指定模块中搜索")
        print("\n示例:")
        print("  python tracking_dict.py module 主页")
        print("  python tracking_dict.py search 点击")
        print("  python tracking_dict.py search 曝光 新闻")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        print("📚 埋点字典模块列表:\n")
        for i, (name, idx) in enumerate(MODULE_MAP.items(), 1):
            print(f"{i:2d}. {name}")
    
    elif cmd == 'module' and len(sys.argv) > 2:
        module_name = sys.argv[2]
        events = get_module_events(module_name)
        
        if events is None:
            print(f"❌ 模块 '{module_name}' 不存在")
            return
        
        print(f"\n📋 模块: {module_name} (共 {len(events)} 个埋点)\n")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.get('event', 'N/A')}")
            print(f"   Type: {event.get('type', 'N/A')}")
            print(f"   Params: {event.get('params', 'N/A')}")
            if event.get('修订记录'):
                print(f"   版本: {event.get('修订记录', '')}")
            print()
    
    elif cmd == 'search':
        keyword = sys.argv[2] if len(sys.argv) > 2 else ''
        module = sys.argv[3] if len(sys.argv) > 3 else None
        
        if not keyword:
            print("❌ 请提供搜索关键词")
            return
        
        results = search_event(keyword, module)
        
        if not results:
            print(f"❌ 未找到包含 '{keyword}' 的埋点")
            return
        
        print(f"\n🔍 搜索结果: '{keyword}' (共 {len(results)} 个)\n")
        for i, event in enumerate(results, 1):
            print(f"{i}. [{event['sheet']}] {event.get('event', 'N/A')}")
            print(f"   Type: {event.get('type', 'N/A')}")
            print(f"   Params: {event.get('params', 'N/A')}")
            print()
    
    else:
        print(f"❌ 未知命令: {cmd}")

if __name__ == '__main__':
    main()
