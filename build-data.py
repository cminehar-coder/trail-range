"""Reproduce the curated dataset, joining fuel economy by explicit EPA record ID."""
import csv, io, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
epa={r['id']:r for r in csv.DictReader(io.TextIOWrapper(zipfile.ZipFile(ROOT.parent/'vehicles.csv.zip').open('vehicles.csv')))}
S={
 'rav4':{'title':'Toyota 2024 RAV4 U.S. brochure','url':'https://www.toyota.com/content/dam/toyota/brochures/pdf/2024/rav4_ebrochure.pdf','location':'Capability and dimensions tables'},
 'crosstrek':{'title':'Subaru 2024 Crosstrek Wilderness launch specifications','url':'https://www.prnewswire.com/news-releases/subaru-debuts-the-all-new-2024-crosstrek-wilderness-at-the-new-york-international-auto-show-301790484.html','location':'Crosstrek and Crosstrek Wilderness comparison table'},
 'forester':{'title':'Subaru 2024 Forester Wilderness brochure','url':'https://www.subaru.com/content/dam/subaru/downloads/pdf/brochures/2024/2024_Forester_Wilderness_Brochure_050824.pdf#page=16','location':'Printed page 15, Dimensions'},
 'foresterTires':{'title':'Subaru 2024 Forester at a glance','url':'https://s3.amazonaws.com/subarumedia.iconicweb.com/mediasite/attachments/24MY_Forester_-_AAG_-_FINALv3.pdf','location':'Wilderness equipment / tires'},
 'outback':{'title':'Subaru 2024 Outback U.S. brochure','url':'https://www.subaru.com/content/dam/subaru/downloads/pdf/brochures/2024/MY24_Outback_Brochure.pdf#page=12','location':'Dimensions; footnote distinguishes non-XT and XT approach angles'},
 'bronco':{'title':'Ford 2021 Bronco U.S. technical specifications','url':'https://www.ford.com/cmslibs/content/dam/brand_ford/en_us/brand/suvs-crossovers/bronco/2021/mediakit/21_Bronco_Prelim_Tech_Specs_1.pdf','location':'Two-door/four-door off-road capability and tire tables; archival Ford URL may redirect'},
 'broncoHardware':{'title':'Ford 2021 Bronco equipment series','url':'https://www.ford.com/cmslibs/content/dam/brand_ford/en_us/brand/suvs-crossovers/bronco/2021/mediakit/21_Bronco_Trims_Sheet_1.pdf','location':'Base and Sasquatch package equipment'},
 'broncoSport':{'title':'Ford 2021 Bronco Sport U.S. technical specifications','url':'https://media.ford.com/content/dam/fordmedia/North%20America/US/product/2021/bronco-sport/pdf/21MY-BroncoSport-Tech-Specs.pdf','location':'Exterior dimensions, standard versus optional tires; archival Ford URL may redirect'},
 'wrangler':{'title':'Jeep 2023 Wrangler Product Information (manufacturer PDF, forum mirror)','url':'https://www.jlwranglerforums.com/forum/attachments/2023_jp_wrangler_sp-5-pdf.926938/','location':'Pages 2, 8–9: powertrain MPG, wheelbase, tire-specific clearances'},
 '4runner':{'title':'Toyota 2015 4Runner U.S. brochure (manufacturer PDF, archive mirror)','url':'https://s3.amazonaws.com/cdn.autoipacket.com/brochures/toyota/2015/2015-toyota-4runner.pdf','location':'Trail specifications, dimensions and off-highway table'},
 'tacoma':{'title':'Toyota 2024 Tacoma Product Information (manufacturer PDF, forum mirror)','url':'https://www.tacoma4g.com/forum/attachments/2024_toyota_tacoma_product_information-pdf.12235/','location':'Page 7: TRD Pro clearance/angles; departure without tow hitch'},
 'tacomaBrochure':{'title':'Toyota 2024 Tacoma U.S. brochure','url':'https://www.toyota.com/content/dam/toyota/brochures/pdf/2024/tacoma_ebrochure.pdf','location':'TRD Pro wheels, hybrid powertrain, short-bed wheelbase'},
 'landcruiser':{'title':'Toyota 2024 Land Cruiser U.S. launch specifications','url':'https://pressroom.toyota.com/the-evolution-of-a-legend-the-all-new-2024-land-cruiser/','location':'Angles, hybrid drivetrain, low range and locking differentials'},
 'landcruiserDimensions':{'title':'Toyota 2024 Land Cruiser U.S. press release (manufacturer PDF, media mirror)','url':'https://cdn.motor1.com/pdf-files/2024-toyota-land-cruiser-press-release-2.pdf','location':'Land Cruiser grade dimensions and tires, not 1958 grade'}
}
V=[]
def add(id,year,make,model,trim,engine,epa_id,clearance,approach,departure,breakover,wheelbase,tire,source,fuel='Gasoline',low=False,rear=False,front=False,notes='',short=None,extra=None):
 r=epa[str(epa_id)];assert int(r['year'])==year;assert r['fuelType1'] in ['Regular Gasoline','Premium Gasoline'];assert not r.get('phevBlended')=='true';assert int(r.get('rangeA') or 0)==0
 tire_source={'title':f'{year} {make} {model} {trim}: original-size tire fitment','url':f'https://www.goodyear.com/en-us/vehicles/{make}/{model.replace(" ","-")}/{year}/{trim.split(" · ")[0].replace(" ","-")}','location':'Cross-check original fitment; dimension score uses nominal sidewall size, not measured loaded diameter'}
 sources={'geometry':[source],'tires':[source],'hardware':[source],'mpg':{'title':f'EPA #{epa_id}: {r["year"]} {r["model"]}, {r["displ"]} L, {r["trany"]}','url':f'https://www.fueleconomy.gov/feg/noframes/{epa_id}.shtml'}}
 if extra:sources['geometry']+=extra
 if model in ['Crosstrek','Outback']:
  fitment='Wilderness' if 'Wilderness' in trim else 'Standard'
  tire_source['url']=f'https://www.goodyear.com/en-us/vehicles/{make}/{model}/{year}/{fitment}'
  sources['tires']=[tire_source]
 if model=='Crosstrek' and 'Base' in trim:
  sources['tires']=[{'title':'Tire Rack: 2024 Crosstrek Base original tire fitment','url':'https://www.tirerack.com/tires/TireSearchResults.jsp?autoMake=Subaru&autoModClar=Base&autoModel=Crosstrek&autoYear=2024&diameter=17&filtering=true&ratio=60&sortCode=49751&width=225%2F','location':'225/60R17 original size'}]
 if model=='RAV4':sources['tires']=[{'title':'Firestone: 2024 RAV4 original tire sizes by trim','url':'https://vehicle.firestonecompleteautocare.com/toyota/rav4/2024/','location':'Original tire-size table; exact trim as listed above'}]
 if model=='Forester':sources['tires']=['foresterTires']
 if model=='Land Cruiser':sources['tires']=['landcruiserDimensions']
 if model=='Bronco':sources['hardware']=['broncoHardware']
 V.append(dict(id=id,year=year,make=make,model=model,trim=trim,engine=engine,fuel=fuel,mpg=int(r['comb08']),city=int(r['city08']),highway=int(r['highway08']),epaId=str(epa_id),epaModel=r['model'],epaTransmission=r['trany'],clearance=clearance,approach=approach,departure=departure,breakover=breakover,wheelbase=wheelbase,tireSize=tire,lowRange=low,rearLocker=rear,frontLocker=front,notes=notes,short=short or model+' '+trim,sources=sources))
add('rav4-hybrid',2024,'Toyota','RAV4','Hybrid LE AWD','2.5 L hybrid / eCVT',47392,8.1,19,21,None,105.9,'225/65R17','rav4',fuel='Hybrid',notes='Published breakover not located. Electric rear axle; no low range. EPA current combined rating is 39, rather than the older 40 MPG figure.',short='RAV4 Hybrid LE')
add('rav4-woodland',2024,'Toyota','RAV4','Hybrid Woodland AWD','2.5 L hybrid / eCVT',47391,8.1,19,21,None,105.9,'225/60R18','rav4',fuel='Hybrid',notes='Factory all-terrain tires and TRD-tuned suspension. Those traction differences are not captured by this geometry-only score. Published breakover not located.',short='RAV4 Woodland')
add('rav4-trd',2024,'Toyota','RAV4','TRD Off-Road AWD','2.5 L / 8-speed automatic',47389,8.6,19,21,None,105.9,'225/60R18','rav4',notes='Torque-vectoring rear AWD; no low range or mechanical axle lockers. Published breakover not located.',short='RAV4 TRD Off-Road')
add('crosstrek-base',2024,'Subaru','Crosstrek','Base AWD','2.0 L / CVT',46540,8.7,18,30.1,19.7,105.1,'225/60R17','crosstrek',short='Crosstrek Base')
add('crosstrek-wilderness',2024,'Subaru','Crosstrek','Wilderness AWD','2.5 L / CVT',47162,9.3,20,33,21.1,104.9,'225/60R17','crosstrek',notes='Dual-mode X-MODE and all-terrain tires. No low-range transfer case.',short='Crosstrek Wilderness')
add('forester-wilderness',2024,'Subaru','Forester','Wilderness AWD','2.5 L / CVT',47163,9.2,23.5,25.4,21,104.9,'225/60R17','forester',notes='Dual-mode X-MODE and all-terrain tires. No low-range transfer case.',short='Forester Wilderness')
add('outback-base',2024,'Subaru','Outback','Base AWD','2.5 L / CVT',46541,8.7,18,21.7,19.4,108.1,'225/65R17','outback',short='Outback Base')
add('outback-wilderness',2024,'Subaru','Outback','Wilderness AWD','2.4 L turbo / CVT',46543,9.5,20,23.6,21.2,108.1,'225/65R17','outback',notes='2024 front/rear bumper geometry; no low-range transfer case.',short='Outback Wilderness')
for doors,wb,gc,dep,br in [(2,100.4,8.4,29.8,21.1),(4,116.1,8.3,29.7,20.0)]:
 add(f'bronco-base-{doors}',2021,'Ford','Bronco',f'Base · {doors}-door','2.3 L turbo / 10-speed automatic',43995,gc,35.5,dep,br,wb,'255/70R16','bronco',low=True,notes='Standard tires and suspension. EPA entry groups body styles; MPG is the configuration-group rating, not a separate body-style test.',short=f'Bronco Base {doors}D')
for doors,wb,gc,dep,br in [(2,100.4,11.6,37.2,29),(4,116.1,11.5,37,26.3)]:
 add(f'bronco-sasquatch-{doors}',2021,'Ford','Bronco',f'Base Sasquatch · {doors}-door','2.3 L turbo / 10-speed automatic',44002,gc,43.2,dep,br,wb,'315/70R17','bronco',low=True,rear=True,front=True,notes='Factory Sasquatch package; no Badlands sway-bar disconnect assumed. EPA groups body styles. Nominal tire diameter is calculated from the sidewall size, not the rounded 35-inch marketing label.',short=f'Bronco Sasquatch {doors}D')
add('bronco-sport-base',2021,'Ford','Bronco Sport','Base AWD','1.5 L turbo / 8-speed automatic',43543,7.8,21.7,30.4,18.2,105.1,'225/65R17','broncoSport',short='Bronco Sport Base')
add('bronco-sport-badlands',2021,'Ford','Bronco Sport','Badlands · optional A/T tires','2.0 L turbo / 8-speed automatic',43544,8.8,30.4,33.1,20.4,105.1,'235/65R17','broncoSport',notes='Optional 235/65R17 package is required for these dimensions. Twin-clutch rear drive is not counted as a mechanical rear locker; no low range. EPA does not separately rate this tire option.',short='Bronco Sport Badlands')
for doors,wb,ap,br,epaid in [(2,96.8,44,27.8,45693),(4,118.4,43.9,22.6,45696)]:
 add(f'wrangler-rubicon-{doors}',2023,'Jeep','Wrangler',f'Rubicon · {doors}-door','3.6 L V6 / 6-speed manual',epaid,10.8,ap,37,br,wb,'285/70R17','wrangler',low=True,rear=True,front=True,notes='Standard 33-inch-class tires; excludes Xtreme Recon and 392. EPA powertrain/body-style entry does not separately name Rubicon. Model-year manufacturer sheet lists this engine/transmission rating.',short=f'Wrangler Rubicon {doors}D')
for doors,wb,br,dep,epaid in [(2,96.8,25,35.9,45691),(4,118.4,20.3,36.1,45694)]:
 add(f'wrangler-sport-{doors}',2023,'Jeep','Wrangler',f'Sport · {doors}-door','2.0 L turbo / 8-speed automatic',epaid,9.7,41.4,dep,br,wb,'245/75R17','wrangler',low=True,notes='Standard Sport geometry and tires; EPA powertrain/body-style group. No optional rear limited-slip differential assumed.',short=f'Wrangler Sport {doors}D')
add('4runner-trail',2015,'Toyota','4Runner','Trail 4WD','4.0 L V6 / 5-speed automatic',35595,9.6,33,26,None,109.8,'265/70R17','4runner',low=True,rear=True,notes='Trail trim, standard suspension. Published breakover not located; optional KDSS is not assumed.',short='4Runner Trail')
add('tacoma-pro',2024,'Toyota','Tacoma','TRD Pro · Double Cab, 5-ft bed','2.4 L hybrid / 8-speed automatic',48461,11.5,35.7,25.3,27.4,131.9,'265/70R18','tacoma',fuel='Hybrid',low=True,rear=True,notes='Manufacturer maximum TRD Pro running clearance. Departure specification is WITHOUT tow hitch; a hitch can reduce it. Dimensions are not directly identical in measurement convention to every other manufacturer.',short='Tacoma TRD Pro',extra=['tacomaBrochure'])
add('landcruiser',2024,'Toyota','Land Cruiser','Land Cruiser grade · 18-in wheels','2.4 L hybrid / 8-speed automatic',47762,8.7,31,22,25,112.2,'265/70R18','landcruiser',fuel='Hybrid',low=True,rear=True,notes='Land Cruiser grade (not 1958), standard 18-inch wheels. Center and rear lockers plus stabilizer disconnect. Initial U.S. manufacturer specification sheet used for geometry.',short='Land Cruiser',extra=['landcruiserDimensions'])
payload={'version':1,'updated':'2026-10-02','scope':'Selected stock U.S. configurations within model years 2015–2025. This seed dataset currently represents 2015, 2021, 2023 and 2024; it is not an exhaustive census or live sale inventory. Gasoline and conventional hybrids only.','sources':S,'vehicles':V}
(ROOT/'public'/'vehicles.json').write_text(json.dumps(payload,indent=2)+'\n')
(ROOT/'public'/'data.js').write_text('window.OFFROAD_DATA = '+json.dumps(payload,ensure_ascii=False,indent=2)+';\n')
(ROOT/'public'/'epa-extract.json').write_text(json.dumps([{k:epa[v['epaId']][k] for k in ['id','year','make','model','displ','trany','fuelType1','comb08','city08','highway08']} for v in V],indent=2)+'\n')
print(f'Built {len(V)} sourced configurations; {sum(v["breakover"] is None for v in V)} missing published breakover.')
