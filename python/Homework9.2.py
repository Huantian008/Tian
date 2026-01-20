def tongzhong(n,start,middle,end):
    if n==1:
        print(f"把第1口铜钟：从{start}->{end}")
        return
    tongzhong(n-1,start,end,middle)
    print(f"把第{n}口铜钟：从{start}->{end}")
    tongzhong(n-1,middle,start,end)
tongzhong(3,"城东","城中","城西")