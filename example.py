from cdr3pairsearch import search_paired_chains

# 示例1: 搜索重链CDR3序列
search_paired_chains(
    database_dir="./database",
    cdr3_aa_heavy="CARDTGGFDIW",
    threshold=1,
    distance_method="edit",
    v_call_heavy="IGHV1-69",
    output_file="./results/heavy_chain_results.csv"
)

# 示例2: 搜索轻链CDR3序列，使用汉明距离
search_paired_chains(
    database_dir="./database",
    cdr3_aa_light="CASSSGIGNAVFGGGTKLTVL",
    threshold=2,
    distance_method="hamming",
    j_call_light="IGLJ3",
    output_file="./results/light_chain_results.csv",
    chunk_size=10000  # 处理大文件时使用
)

# 示例3: 使用通用CDR3搜索
search_paired_chains(
    database_dir="./database",
    cdr3_aa="CARDTGGFDIW",
    threshold=1,
    output_file="./results/general_cdr3_results.csv"
)
