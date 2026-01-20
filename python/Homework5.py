id_str=(
    'id="4301,长沙市;4302,株洲市;4303,湘潭市;4304,衡阳市;4305,邵阳市;4306,岳阳市;'
    '4307,常德市;4308,张家界市;4309,益阳市;4310,郴州市;4311,永州市;4312,怀化市;'
    '4313,娄底市;4321,株洲市;4322,岳阳地区;4323,益阳市;4325,娄底市;4326,邵阳市;'
    '4327,衡阳市;4328,郴州市;4329,永州市;4330,怀化市;"'
)
clean=id_str.strip()
if clean.startswith('id="'):
    clean=clean[4:]
if clean.endswith('"'):    
    clean=clean[:-1]
pairs_raw=clean.split(';')
pairs_raw=[p for p in pairs_raw if p]
codes=[]
cities=[]
for pair in pairs_raw:
    if ','in pair:
        code,city=pair.split(',',1)
        codes.append(code.strip())
        cities.append(city.strip())
print(codes)
print(cities)