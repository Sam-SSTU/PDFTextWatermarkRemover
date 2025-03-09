# -*- coding: utf-8 -*-
"""
给定一个pdf路径，以及一个列表，可修改pdf内容，删除所有符合条件的文字。
"""

import re
import os
import pikepdf
from pikepdf import Pdf, PdfImage, Name, Dictionary, Object

# 默认水印关键词列表
DEFAULT_WATERMARK_KEYWORDS = [
    "Review Copy",
    "University Press",
    "Copyright Material",
    "Review Only",
    "Not for Redistribution",
    "International"
]

# 当前使用的水印关键词列表
WATERMARK_KEYWORDS = DEFAULT_WATERMARK_KEYWORDS.copy()

# 调试模式
DEBUG = True

def set_watermark_keywords(keywords):
    """设置新的水印关键词列表"""
    global WATERMARK_KEYWORDS
    WATERMARK_KEYWORDS = keywords

def get_watermark_keywords():
    """获取当前水印关键词列表"""
    return WATERMARK_KEYWORDS

def get_default_watermark_keywords():
    """获取默认水印关键词列表"""
    return DEFAULT_WATERMARK_KEYWORDS

def reset_watermark_keywords():
    """重置为默认水印关键词列表"""
    global WATERMARK_KEYWORDS
    WATERMARK_KEYWORDS = DEFAULT_WATERMARK_KEYWORDS.copy()

def debug_print(message):
    """调试信息打印"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def count_watermarks_in_text(text):
    """统计文本中的水印数量"""
    watermark_count = 0
    watermark_details = {}
    
    for keyword in WATERMARK_KEYWORDS:
        # 使用正则表达式查找所有匹配项
        matches = re.findall(keyword, text, re.IGNORECASE)
        if matches:
            count = len(matches)
            watermark_count += count
            watermark_details[keyword] = count
    
    return watermark_count, watermark_details

def check_for_watermarks(pdf_path):
    """检查PDF中是否存在水印，并详细统计每页的水印数量"""
    try:
        with pikepdf.open(pdf_path) as pdf:
            total_watermark_count = 0
            pages_with_watermarks = set()
            watermarks_per_page = {}
            
            print(f"检查文件中的水印: {pdf_path}")
            
            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                print(f"\r检查页面 {page_num}/{len(pdf.pages)}", end="")
                
                # 提取页面文本
                text = ""
                try:
                    # 尝试获取页面内容
                    if page.get("/Contents") is not None:
                        content_stream = page.get("/Contents")
                        if isinstance(content_stream, list):
                            for obj in content_stream:
                                text += obj.read_bytes().decode('utf-8', errors='ignore')
                        else:
                            text += content_stream.read_bytes().decode('utf-8', errors='ignore')
                except Exception as e:
                    print(f"\n提取页面 {page_num} 文本时出错: {str(e)}")
                
                # 统计页面中的水印数量
                page_watermark_count, watermark_details = count_watermarks_in_text(text)
                
                if page_watermark_count > 0:
                    total_watermark_count += page_watermark_count
                    pages_with_watermarks.add(page_num)
                    watermarks_per_page[page_num] = (page_watermark_count, watermark_details)
            
            print(f"\n\n检查完成: 发现总计 {total_watermark_count} 处水印，在 {len(pages_with_watermarks)} 个页面")
            
            # 显示每页的水印统计
            if watermarks_per_page:
                print("\n每页水印统计:")
                for page_num in sorted(watermarks_per_page.keys()):
                    count, details = watermarks_per_page[page_num]
                    print(f"  页面 {page_num}: {count} 处水印")
                    for keyword, keyword_count in details.items():
                        print(f"    - '{keyword}': {keyword_count} 处")
            
            if pages_with_watermarks:
                print(f"\n包含水印的页面: {', '.join(map(str, sorted(pages_with_watermarks)))}")
            
            return total_watermark_count, pages_with_watermarks, watermarks_per_page
    except Exception as e:
        print(f"检查水印时出错: {str(e)}")
        return 0, set(), {}

def extreme_watermark_removal(input_path, output_path):
    """使用极端方法移除所有形式的水印，包括半透明背景水印"""
    try:
        with pikepdf.open(input_path) as pdf:
            modified_pages = 0
            
            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                print(f"\r处理页面 {page_num}/{len(pdf.pages)}", end="")
                page_modified = False
                
                # 1. 移除页面中的所有XObject（可能包含水印图像）
                if "/Resources" in page:
                    resources = page["/Resources"]
                    
                    # 处理XObject资源
                    if "/XObject" in resources:
                        # 保存原始XObject引用
                        original_xobjects = resources["/XObject"]
                        
                        # 创建新的XObject字典，只保留不包含水印的对象
                        new_xobjects = pikepdf.Dictionary()
                        for name, xobject in original_xobjects.items():
                            keep_object = True
                            
                            try:
                                # 检查XObject内容
                                if xobject.get("/Subtype") == "/Form":
                                    # 尝试读取XObject内容
                                    content = ""
                                    try:
                                        if "/Contents" in xobject:
                                            content = xobject["/Contents"].read_bytes().decode('utf-8', errors='ignore')
                                        else:
                                            content = xobject.read_bytes().decode('utf-8', errors='ignore')
                                    except:
                                        pass
                                    
                                    # 检查是否包含水印关键词
                                    for keyword in WATERMARK_KEYWORDS:
                                        if keyword.lower() in content.lower():
                                            keep_object = False
                                            debug_print(f"移除页面 {page_num} 中的水印XObject: {name}")
                                            page_modified = True
                                            break
                            except Exception as e:
                                debug_print(f"处理XObject时出错: {str(e)}")
                            
                            # 如果不包含水印，保留该对象
                            if keep_object:
                                new_xobjects[name] = xobject
                        
                        # 更新资源字典中的XObject
                        resources["/XObject"] = new_xobjects
                
                # 2. 处理内容流，只移除包含水印关键词的文本块
                if "/Contents" in page:
                    content_stream = page["/Contents"]
                    
                    if isinstance(content_stream, list):
                        new_contents = []
                        
                        for obj in content_stream:
                            try:
                                content_bytes = obj.read_bytes()
                                content_str = content_bytes.decode('utf-8', errors='ignore')
                                
                                # 找到所有文本块（BT...ET之间的内容）
                                text_blocks = re.findall(r'(BT.*?ET)', content_str, flags=re.DOTALL)
                                modified_content = content_str
                                
                                for block in text_blocks:
                                    # 检查文本块是否包含水印关键词
                                    contains_watermark = False
                                    for keyword in WATERMARK_KEYWORDS:
                                        if keyword.lower() in block.lower():
                                            contains_watermark = True
                                            break
                                    
                                    # 只删除包含水印关键词的文本块
                                    if contains_watermark:
                                        modified_content = modified_content.replace(block, '')
                                        debug_print(f"在页面 {page_num} 中移除包含水印的文本块")
                                        page_modified = True
                                
                                # 如果内容有变化，添加到新内容列表
                                if modified_content.strip():
                                    new_contents.append(pikepdf.Stream(pdf, modified_content.encode('utf-8')))
                            except Exception as e:
                                debug_print(f"处理内容流时出错: {str(e)}")
                                new_contents.append(obj)
                        
                        if new_contents:
                            page["/Contents"] = new_contents
                    else:
                        try:
                            content_bytes = content_stream.read_bytes()
                            content_str = content_bytes.decode('utf-8', errors='ignore')
                            
                            # 找到所有文本块（BT...ET之间的内容）
                            text_blocks = re.findall(r'(BT.*?ET)', content_str, flags=re.DOTALL)
                            modified_content = content_str
                            
                            for block in text_blocks:
                                # 检查文本块是否包含水印关键词
                                contains_watermark = False
                                for keyword in WATERMARK_KEYWORDS:
                                    if keyword.lower() in block.lower():
                                        contains_watermark = True
                                        break
                                
                                # 只删除包含水印关键词的文本块
                                if contains_watermark:
                                    modified_content = modified_content.replace(block, '')
                                    debug_print(f"在页面 {page_num} 中移除包含水印的文本块")
                                    page_modified = True
                            
                            # 如果内容有变化，更新内容流
                            if modified_content.strip():
                                page["/Contents"] = pikepdf.Stream(pdf, modified_content.encode('utf-8'))
                        except Exception as e:
                            debug_print(f"处理内容流时出错: {str(e)}")
                
                # 3. 移除页面中的所有注释（可能包含水印）
                if "/Annots" in page:
                    del page["/Annots"]
                    page_modified = True
                
                # 4. 移除页面中的所有可能包含水印的元数据
                for key in ["/Metadata", "/PieceInfo"]:
                    if key in page:
                        del page[key]
                        page_modified = True
                
                # 5. 处理页面的图形状态参数字典
                if "/Resources" in page and "/ExtGState" in page["/Resources"]:
                    # 移除透明度设置，这可能用于水印
                    del page["/Resources"]["/ExtGState"]
                    page_modified = True
                
                if page_modified:
                    modified_pages += 1
            
            # 6. 移除文档级别的元数据
            if "/Metadata" in pdf.Root:
                del pdf.Root["/Metadata"]
            
            # 7. 移除文档信息字典
            if "/Info" in pdf.trailer:
                del pdf.trailer["/Info"]
            
            # 保存修改后的PDF
            pdf.remove_unreferenced_resources()
            pdf.save(output_path)
            
            print(f"\n\n成功保存PDF到: {output_path}")
            print(f"已修改 {modified_pages} 页")
            
            return modified_pages
    except Exception as e:
        print(f"移除水印时出错: {str(e)}")
        return 0

def create_clean_pdf(input_path, output_path):
    """创建一个全新的PDF，只保留原始内容，彻底移除水印"""
    try:
        # 创建一个临时文件路径
        temp_path = output_path + ".temp.pdf"
        
        # 首先使用极端方法处理水印
        extreme_watermark_removal(input_path, temp_path)
        
        # 然后创建一个全新的PDF，只保留文本和图像内容
        with pikepdf.open(temp_path) as src_pdf:
            dst_pdf = pikepdf.new()
            
            # 复制每一页，但只保留必要的内容
            for i, src_page in enumerate(src_pdf.pages):
                page_num = i + 1
                print(f"\r重建页面 {page_num}/{len(src_pdf.pages)}", end="")
                
                # 创建新页面
                dst_page = dst_pdf.add_blank_page(
                    width=src_page.MediaBox[2],
                    height=src_page.MediaBox[3]
                )
                
                # 复制页面的基本属性
                for key in ["/MediaBox", "/CropBox", "/Rotate"]:
                    if key in src_page:
                        dst_page[key] = src_page[key]
                
                # 创建新的资源字典
                dst_page["/Resources"] = pikepdf.Dictionary()
                
                # 复制字体资源
                if "/Resources" in src_page and "/Font" in src_page["/Resources"]:
                    dst_page["/Resources"]["/Font"] = src_page["/Resources"]["/Font"]
                
                # 复制内容流，但过滤掉水印
                if "/Contents" in src_page:
                    content_stream = src_page["/Contents"]
                    
                    if isinstance(content_stream, list):
                        new_contents = []
                        
                        for obj in content_stream:
                            try:
                                content_bytes = obj.read_bytes()
                                content_str = content_bytes.decode('utf-8', errors='ignore')
                                
                                # 检查是否包含水印关键词
                                contains_watermark = False
                                for keyword in WATERMARK_KEYWORDS:
                                    if keyword.lower() in content_str.lower():
                                        contains_watermark = True
                                        break
                                
                                # 如果不包含水印，保留该内容
                                if not contains_watermark:
                                    new_contents.append(pikepdf.Stream(dst_pdf, content_bytes))
                            except:
                                # 如果处理出错，保留原始内容
                                new_contents.append(pikepdf.Stream(dst_pdf, obj.read_bytes()))
                        
                        if new_contents:
                            dst_page["/Contents"] = new_contents
                    else:
                        try:
                            content_bytes = content_stream.read_bytes()
                            content_str = content_bytes.decode('utf-8', errors='ignore')
                            
                            # 检查是否包含水印关键词
                            contains_watermark = False
                            for keyword in WATERMARK_KEYWORDS:
                                if keyword.lower() in content_str.lower():
                                    contains_watermark = True
                                    break
                            
                            # 如果不包含水印，保留该内容
                            if not contains_watermark:
                                dst_page["/Contents"] = pikepdf.Stream(dst_pdf, content_bytes)
                        except:
                            # 如果处理出错，保留原始内容
                            dst_page["/Contents"] = pikepdf.Stream(dst_pdf, content_stream.read_bytes())
            
            # 保存新的PDF
            dst_pdf.save(output_path)
            
            # 删除临时文件
            try:
                os.remove(temp_path)
            except:
                pass
            
            print(f"\n\n成功创建干净的PDF: {output_path}")
            print(f"总页数: {len(dst_pdf.pages)}")
            
            return len(dst_pdf.pages)
    except Exception as e:
        print(f"创建干净PDF时出错: {str(e)}")
        return 0

def main():
    """读取PDF，移除水印，并保存为新文件"""
    input_path = "Original-pdf/Original.pdf"
    output_path = "Output-pdf/Output.pdf"
    
    print(f"读取文件: {input_path}")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # 检查原始文件中的水印
        print("\n--- 详细检查原始文件中的水印 ---")
        original_watermarks, pages_with_watermarks, watermarks_per_page = check_for_watermarks(input_path)
        
        if original_watermarks == 0:
            print("原始文件中未检测到水印，无需处理")
            return
        
        # 计算每页平均水印数量
        avg_watermarks_per_page = original_watermarks / len(pages_with_watermarks) if pages_with_watermarks else 0
        print(f"\n平均每页水印数量: {avg_watermarks_per_page:.2f}")
        
        # 使用极端方法移除水印
        print("\n--- 使用极端方法移除所有形式的水印 ---")
        modified_pages = extreme_watermark_removal(input_path, output_path)
        
        if modified_pages == 0:
            print("使用极端方法未能修改任何页面，尝试创建全新的PDF")
            
            # 尝试创建全新的PDF
            print("\n--- 创建全新的PDF，彻底移除水印 ---")
            create_clean_pdf(input_path, output_path)
        
        # 检查处理后文件中的水印
        print("\n--- 检查处理后文件中的水印 ---")
        remaining_watermarks, remaining_pages, remaining_watermarks_per_page = check_for_watermarks(output_path)
        
        if remaining_watermarks == 0:
            print("所有水印已成功移除！")
        else:
            print(f"警告: 仍有 {remaining_watermarks} 处水印未被移除，在 {len(remaining_pages)} 个页面")
            
            # 显示移除效果
            removal_rate = 100 * (1 - remaining_watermarks / original_watermarks)
            print(f"\n水印移除率: {removal_rate:.2f}%")
            
            # 如果仍有水印，尝试创建全新的PDF
            if removal_rate < 100:
                print("\n--- 尝试创建全新的PDF，彻底移除水印 ---")
                create_clean_pdf(input_path, output_path)
                
                # 再次检查
                print("\n--- 最终检查处理后文件中的水印 ---")
                final_watermarks, final_pages, _ = check_for_watermarks(output_path)
                
                if final_watermarks == 0:
                    print("所有水印已成功移除！")
                else:
                    print(f"警告: 仍有 {final_watermarks} 处水印未被移除，在 {len(final_pages)} 个页面")
                    final_removal_rate = 100 * (1 - final_watermarks / original_watermarks)
                    print(f"\n最终水印移除率: {final_removal_rate:.2f}%")
            
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()