Search.setIndex({docnames:["about","anatomy_of_ichnosat_platform","contacts","credits","documentation","downloads","how_to_configure","how_to_create_a_new_plugin","how_to_monitor_activities","how_to_restore_the_database","how_to_run","how_to_stop","index","installation_and_requirements","introduction","modules","overview","software_architecture","src","src.core","src.core.downloader","src.core.processing_pipe","src.core.processing_pipe.scientific_processor","src.core.processing_pipe.scientific_processor.src","src.core.processing_pipe.src","src.core.system_manager","src.data","src.data.database","src.data.database.entities","src.data.database.services","src.data.logger","src.presentation","src.presentation.external_interface","src.tests","src.tests.downloader","tutorial"],envversion:51,filenames:["about.rst","anatomy_of_ichnosat_platform.rst","contacts.rst","credits.rst","documentation.rst","downloads.rst","how_to_configure.rst","how_to_create_a_new_plugin.rst","how_to_monitor_activities.rst","how_to_restore_the_database.rst","how_to_run.rst","how_to_stop.rst","index.rst","installation_and_requirements.rst","introduction.rst","modules.rst","overview.rst","software_architecture.rst","src.rst","src.core.rst","src.core.downloader.rst","src.core.processing_pipe.rst","src.core.processing_pipe.scientific_processor.rst","src.core.processing_pipe.scientific_processor.src.rst","src.core.processing_pipe.src.rst","src.core.system_manager.rst","src.data.rst","src.data.database.rst","src.data.database.entities.rst","src.data.database.services.rst","src.data.logger.rst","src.presentation.rst","src.presentation.external_interface.rst","src.tests.rst","src.tests.downloader.rst","tutorial.rst"],objects:{"":{src:[18,0,0,"-"]},"src.core":{downloader:[20,0,0,"-"],processing_pipe:[21,0,0,"-"],system_manager:[25,0,0,"-"]},"src.core.downloader":{AmazonBucketManager:[20,0,0,"-"],Configuration:[20,0,0,"-"],ConfigurationManager:[20,0,0,"-"],Datasource:[20,0,0,"-"],Downloader:[20,0,0,"-"],DownloaderJob:[20,0,0,"-"],ProductDownloader:[20,0,0,"-"],SearchFilter:[20,0,0,"-"]},"src.core.downloader.AmazonBucketManager":{AmazonBucketManager:[20,1,1,""]},"src.core.downloader.AmazonBucketManager.AmazonBucketManager":{extract_date:[20,2,1,""],generate_url:[20,2,1,""],get_products_list:[20,2,1,""],load_products:[20,2,1,""]},"src.core.downloader.Configuration":{Configuration:[20,1,1,""]},"src.core.downloader.ConfigurationManager":{ConfigurationManager:[20,1,1,""]},"src.core.downloader.ConfigurationManager.ConfigurationManager":{datetime_from_string:[20,2,1,""],get_configuration:[20,2,1,""],load_aws_domain:[20,2,1,""],load_aws_products_regex:[20,2,1,""],load_aws_xmlns:[20,2,1,""],load_configuration:[20,2,1,""],load_end_date:[20,2,1,""],load_files_to_download:[20,2,1,""],load_inbox_path:[20,2,1,""],load_parallel_downloads:[20,2,1,""],load_start_date:[20,2,1,""],load_tiles:[20,2,1,""]},"src.core.downloader.Datasource":{Datasource:[20,1,1,""]},"src.core.downloader.Datasource.Datasource":{download_product:[20,2,1,""],get_products_list:[20,2,1,""]},"src.core.downloader.Downloader":{Downloader:[20,1,1,""]},"src.core.downloader.Downloader.Downloader":{create_search_filter:[20,2,1,""],start:[20,2,1,""]},"src.core.downloader.DownloaderJob":{DownloaderJob:[20,1,1,""]},"src.core.downloader.DownloaderJob.DownloaderJob":{refresh_configurations:[20,2,1,""],run:[20,2,1,""]},"src.core.downloader.ProductDownloader":{ProductDownloader:[20,1,1,""]},"src.core.downloader.ProductDownloader.ProductDownloader":{download_product:[20,2,1,""]},"src.core.downloader.SearchFilter":{SearchFilter:[20,1,1,""]},"src.core.processing_pipe":{scientific_processor:[22,0,0,"-"],src:[24,0,0,"-"]},"src.core.processing_pipe.scientific_processor":{src:[23,0,0,"-"]},"src.core.processing_pipe.scientific_processor.src":{start:[23,0,0,"-"]},"src.core.processing_pipe.scientific_processor.src.start":{main:[23,3,1,""],process_req:[23,3,1,""]},"src.core.processing_pipe.src":{Job:[24,0,0,"-"],JobDispatcher:[24,0,0,"-"],Plugin:[24,0,0,"-"],PluginManager:[24,0,0,"-"],ProcessingPipeManager:[24,0,0,"-"]},"src.core.processing_pipe.src.Job":{Job:[24,1,1,""]},"src.core.processing_pipe.src.Job.Job":{fibonacci:[24,2,1,""],run:[24,2,1,""]},"src.core.processing_pipe.src.JobDispatcher":{JobDispatcher:[24,1,1,""]},"src.core.processing_pipe.src.JobDispatcher.JobDispatcher":{run:[24,2,1,""]},"src.core.processing_pipe.src.Plugin":{Plugin:[24,1,1,""]},"src.core.processing_pipe.src.Plugin.Plugin":{more_data:[24,2,1,""],read_pipe:[24,2,1,""],run:[24,2,1,""]},"src.core.processing_pipe.src.PluginManager":{PluginManager:[24,1,1,""]},"src.core.processing_pipe.src.PluginManager.PluginManager":{compile_plugins:[24,2,1,""],get_plugins:[24,2,1,""]},"src.core.processing_pipe.src.ProcessingPipeManager":{ProcessingPipeManager:[24,1,1,""]},"src.core.processing_pipe.src.ProcessingPipeManager.ProcessingPipeManager":{notify_to_scientific_processor:[24,2,1,""],process_product:[24,2,1,""],start_processing:[24,2,1,""]},"src.core.system_manager":{cli:[25,0,0,"-"],system_manager:[25,0,0,"-"]},"src.core.system_manager.system_manager":{SystemManager:[25,1,1,""]},"src.core.system_manager.system_manager.SystemManager":{compile_plugins:[25,2,1,""],create_database:[25,2,1,""],fix_inconsistent_data_in_db:[25,2,1,""],get_downloaded_products:[25,2,1,""],get_downloading_products:[25,2,1,""],get_pending_products:[25,2,1,""],get_processed_products:[25,2,1,""],get_processing_products:[25,2,1,""],is_first_installation:[25,2,1,""],set_first_installation_config:[25,2,1,""],trigger_downloader:[25,2,1,""]},"src.data":{database:[27,0,0,"-"],logger:[30,0,0,"-"]},"src.data.database":{base:[27,0,0,"-"],db:[27,0,0,"-"],entities:[28,0,0,"-"],services:[29,0,0,"-"]},"src.data.database.db":{DB:[27,1,1,""]},"src.data.database.db.DB":{create_db:[27,2,1,""]},"src.data.database.entities":{product:[28,0,0,"-"]},"src.data.database.entities.product":{Product:[28,1,1,""],ProductStatus:[28,1,1,""]},"src.data.database.entities.product.Product":{id:[28,4,1,""],last_modify:[28,4,1,""],name:[28,4,1,""],status:[28,4,1,""]},"src.data.database.entities.product.ProductStatus":{downloaded:[28,4,1,""],downloading:[28,4,1,""],pending:[28,4,1,""],processed:[28,4,1,""],processing:[28,4,1,""]},"src.data.database.services":{products_service:[29,0,0,"-"]},"src.data.database.services.products_service":{ProductsService:[29,1,1,""]},"src.data.database.services.products_service.ProductsService":{add_new_product:[29,2,1,""],get_a_downloaded_product:[29,2,1,""],get_downloaded_products:[29,2,1,""],get_downloading_products:[29,2,1,""],get_pending_products:[29,2,1,""],get_processed_products:[29,2,1,""],get_processing_products:[29,2,1,""],get_products_to_process:[29,2,1,""],update_product_status:[29,2,1,""]},"src.data.logger":{logger:[30,0,0,"-"]},"src.presentation":{external_interface:[32,0,0,"-"]},"src.presentation.external_interface":{start:[32,0,0,"-"]},"src.presentation.external_interface.start":{compile_plugins:[32,3,1,""],create_database:[32,3,1,""],fix_inconsistent_data:[32,3,1,""],get_downloaded_products:[32,3,1,""],get_downloading_products:[32,3,1,""],get_pending_products:[32,3,1,""],get_processed_products:[32,3,1,""],get_processing_products:[32,3,1,""],is_first_installation:[32,3,1,""],start_downloader_interface:[32,3,1,""]},"src.tests":{downloader:[34,0,0,"-"]},src:{core:[19,0,0,"-"],data:[26,0,0,"-"],presentation:[31,0,0,"-"],tests:[33,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:attribute"},terms:{"char":7,"class":[20,24,25,27,28,29],"const":7,"enum":28,"float":7,"import":10,"int":7,"new":[4,12,13,17],"null":7,"public":7,"return":7,"void":[7,10],"while":10,AWS:[0,12],For:17,The:[3,6,7,10,12,17],These:7,Using:6,___:7,____:7,_____:7,______:7,__myplugin_class_h__:7,abl:13,about:[7,17],accept:10,add_new_product:29,addit:13,addon:13,adfgeotransform:7,agendaless:3,algorithm:[7,17],all:[0,7,17],alloc:7,also:[7,10,13],amazonbucketmanag:[17,18,19],anatomi:17,antonin:3,api:[4,12,28],appear:10,architectur:[4,12],archiv:13,armin:3,attribut:7,author:3,auto:17,autogener:[7,12],automat:[0,12,17],avail:[0,7,10,12,17],aws:0,b04:6,b08:6,band01:7,band4_dataset:7,band4_path:7,band:7,bar:10,base:[0,7,12,17,18,20,24,25,26,28,29],bash:[10,13],basi:17,basic:13,been:10,belgium:3,benoit:3,block:13,brandl:3,bua:[2,12],build:[13,17],button:[7,10],calcul:7,can:[6,10],care:7,catholiqu:3,cfg:[6,17],check:10,cli:[17,18,19],click:[7,10],client:[6,10],clima:[2,12],close:7,code:[0,7,12,13],com:[3,13],comma:6,command:[10,13],comment:12,compil:[7,12],compile_plugin:[7,24,25,32],complet:7,compon:17,compos:[6,7,10,11,13,17],comput:3,concat_str:7,conf:17,config:6,configur:[0,4,7,12,17,18,19],configurationmanag:[17,18,19],connect:10,consid:6,consol:13,constant:7,consult:3,contact:12,contain:[0,7,10,11,12,17],content:[12,15,17],contributor:3,convent:12,copi:7,copyright:[3,7],core:[6,7,15,17,18],could:[7,10],cout:7,cpl_port:7,cplerr:7,cplfree:7,cplmalloc:7,creat:[4,10,12,13,17],create_databas:[25,32],create_db:27,create_search_filt:20,creation:[10,17],credit:12,cron:12,crontab:[3,17],cross:[0,12],current:[0,6,10,11,12,13],customiz:[0,12],cycl:6,daniel:3,data:[0,7,10,12,13,15,17,18],data_loc:[7,10,17],databas:[10,12,18,26],dataset:7,datasourc:[17,18,19],date:[0,6,10,12],date_str:20,datetime_from_str:20,debian:17,declar:[17,28],defin:[6,7],definit:[7,17],deleg:24,depend:[13,17],deput:17,descamp:3,descript:17,design:12,destination_path:7,detail:[10,17],develop:[3,7,12,13,17],devic:3,dialog:10,differ:[7,10],directori:[7,10,11,13],doc:[3,17],docker:[0,3,6,7,10,11,12,13,17],dockerfil:17,document:[12,13],domain:20,done:10,doubl:7,down:11,download:[0,7,18,19,28,33],download_product:20,downloaderjob:[17,18,19],driver:7,dynam:[7,17],each:[0,12,17],easi:0,echo:10,edit:6,end:[6,17],end_dat:[6,20],endif:7,endl:7,enough:7,entiti:[17,18,26,27],environ:[7,17],err:7,everi:[6,7,10,17],exampl:[6,10,13,17],expect:7,exploit:[0,6,12],expos:7,ext:28,extend:[0,12,13,17],extens:7,external_interfac:[17,18,31],extract:7,extract_d:20,facilit:12,fals:20,federico:3,fibonacci:24,file:[0,7,10,12,17],file_path:24,files_to_download:[6,20],filter:[6,17],find:10,finish:10,first:10,fix_inconsistent_data:32,fix_inconsistent_data_in_db:25,flask:[3,17],folder:[7,10,11,13],follow:[7,10,13,17],format:7,foundat:3,framework:17,frank:3,free:[3,10],from:[0,7,12,13],fulli:[0,12],ga_readonli:7,gadl:7,gdal:[0,3,7,12,13,17],gdalallregist:7,gdalclos:7,gdaldataset:7,gdaldataseth:7,gdaldriv:7,gdalopen:7,gdalrasterband:7,gdt_float32:7,gener:7,generate_url:20,geo:7,georg:3,geotiff:7,get:[0,7,12],get_a_downloaded_product:29,get_configur:20,get_downloaded_product:[25,29,32],get_downloading_product:[25,29,32],get_pending_product:[25,29,32],get_plugin:24,get_processed_product:[25,29,32],get_processing_product:[25,29,32],get_products_list:20,get_products_to_process:29,getdriverbynam:7,getgdaldrivermanag:7,getgeotransform:7,getprojectionref:7,getrasterband:7,getxsiz:7,getys:7,gf_write:7,github:[0,13,17],global:3,goal:17,going:10,graphic:[7,12],graphica:10,gregorio:3,group:3,gui:[6,17],guid:13,has:10,have:[10,13],haven:7,high:17,how:[4,12,17],html:6,http:[3,10,12,13,17],ichnosat:[0,6,7,13,17],ifndef:7,imag:[3,6,7,13,17],implement:17,inbox:[10,17],inbox_path:20,inc:3,includ:[7,12],inclus:7,index:[7,10],info:2,inform:7,init:[17,18,19],initd:3,input:7,input_file1_path:7,input_filename_1:7,insid:7,instal:[4,7,10,11,12],interfac:[10,12,17],intern:17,interv:[0,12,17],introduct:17,involv:17,iostream:7,is_first_instal:[25,32],isometr:3,item:[10,20],job:[17,18,19,21],jobdispatch:[17,18,19,21],jp2:[6,7],jpeg2000:17,just:7,kei:6,knoledg:13,kwarg:28,label:7,languag:13,last_modifi:28,launch:6,left:10,level:17,librari:[0,12,13,17],licens:[7,12,17],light:17,like:10,limit:7,line:10,link:3,linux:[6,17],list:[6,10,12,17],load:[7,10],load_aws_domain:20,load_aws_products_regex:20,load_aws_xmln:20,load_configur:20,load_end_d:20,load_files_to_download:20,load_inbox_path:20,load_parallel_download:20,load_product:20,load_start_d:20,load_til:20,local:13,localhost:10,locat:[7,10],lock:24,log:[7,17],logger:[17,18,26],lot:13,louvain:3,machin:13,macq:3,main:[17,23],make:7,manag:[6,7,12],martin:3,master:13,matrix:7,max_valu:24,mean:[6,17],memori:7,menu:10,method:17,minut:13,mit:[12,17],mkdir:13,modul:[7,10,12,15,17],monitor:17,more:17,more_data:24,mount:17,move:13,multithread:[0,12],must:[7,10],myplugin:7,name:[7,10,28],ndvi:[0,7,10,12],need:13,new_statu:25,nginx:[6,17],normal:[7,10],note:10,notify_to_scientific_processor:24,now:[6,10],npo:12,number:[0,6,12,17],nvdi_dataset:7,nxsize:7,nysiz:7,object:[20,24,25,27,29],offici:13,open:[0,7,12],openjpeg:3,openjpg:17,oper:13,org:3,orm:17,other:17,our:7,outbox:[10,17],outbox_path:24,output:7,output_dataset:7,owen:3,packag:[12,13,15,17],page:[10,17],pagin:20,parallel:[0,12],parallel_download:6,parallel_process:6,part:17,path:7,pend:[10,28],pep:12,period:6,pip:[3,17],pipe:[0,7],platform:[0,12,13,17],pleas:17,plugin:[0,4,10,12,17,18,19,21],plugin_nam:24,plugin_path:24,pluginmanag:[7,17,18,19,21],plugins_path:24,pocoo:3,podriv:7,pool:17,port:10,portal:[0,12],possibl:[6,7,17],post:17,postgr:10,postgresql:[3,17],prefer:10,present:[7,10,15,17,18],preview:3,primari:13,privat:7,process:[0,7,12,13,17,28],process_algorithm:7,process_product:24,process_req:23,processing_pip:[6,7,17,18,19],processingpipemanag:[17,18,19,21],processor:[0,10,12],product:[0,6,7,12,17,18,20,26,27,29],product_nam:[20,24,29],product_path:7,productdownload:[17,18,19],products_servic:[17,18,26,27],productsservic:29,productstatu:28,professor:3,program:[10,13],progress:10,project:[3,7,17],properti:[0,6,12],prototyp:7,provid:[0,10,12],psycopg2:3,psycopg:3,pszproject:7,purpos:[13,17],put:7,pypi:3,python3:3,python:[0,3,12,13,17],queri:10,queue:20,raffael:[2,12],raffaelebua:2,raster:7,rasterio:7,read:7,read_pip:24,readi:10,readm:17,receiv:[0,10,12,17],refresh_configur:20,releas:[7,12],repositori:12,repres:17,request:17,requir:[4,12],result:7,retriev:17,ronach:3,run:[4,6,7,11,12,17,20,24],same:[0,6,12],sardegna:[2,12],sardegnaclimaonlu:13,satellit:[0,10,12,13,17],save:7,schedul:12,scientific_processor:[7,17,18,19,21],script:10,searchfilt:[17,18,19],section:[7,17],see:10,sens:[0,10,12,17],sentinel:[0,12],separ:6,server:[10,17],servic:[17,18,26,27],set:[10,11,13,17],set_first_installation_config:25,setgeotransform:7,setproject:7,setup:7,share:[0,6,7,12,17],show:12,shown:10,side:10,simpl:17,sinc:13,size:10,sizeof:7,sleep:10,snippet:7,softwar:[3,4,12],sourc:[0,7,12,13,17,20,23,24,25,27,28,29,32],sphinx:[3,12,17],spread:17,sqlalchemi:[3,17,28],src:[6,7,12,17],start:[6,7,10,12,17,18,19,20,21,22,31],start_dat:[6,20],start_downloader_interfac:32,start_process:24,statu:[28,29],std:7,stdio:7,stdlib:7,step:[7,10,13],stop:[4,12],stream:[7,10],string:[6,7],structur:[7,13],submodul:[17,18,19,21,22,26,31],subpackag:[12,15,17],supervisord:[3,17],support:[0,12],system:[6,10,12,13],system_manag:[6,17,18,19],systemmanag:25,tail:10,take:13,task:17,team:3,temporari:17,termin:10,test:[12,17],text:17,them:[7,17],thi:[0,6,7,10,12,13,17],third:17,thread:[17,20,24],tile:[0,10,12,17,20],time:[0,10,12,17],tranform:7,trigger_download:25,tutori:[12,17],txt:17,ucl:3,under:12,understand:13,unit:12,universit:3,unix:10,unus:7,unzip:13,update_product_statu:29,use:[7,13],used:17,user:[7,10,12,17],using:[6,13],usr:[6,7,10,11,13],valgrind:[3,17],varrazzo:3,vector:3,veget:[7,10],vendor:17,version:[0,10,12,17],vexel:3,via:[0,7,12,17],vim:6,virtual:17,visit:17,voic:10,volum:6,wait:10,want:[13,17],warmerdam:3,watch:10,web:[12,17],webserv:17,wget:13,when:[7,10,17],where:[7,10],which:13,work:[13,17],workflow:17,write:7,written:[0,7,12],www:3,year:20,yml:[6,17],you:[6,7,10,13,17],your:[7,10,13,17],yournam:7,zip:13},titles:["About","Anatomy of Ichnosat Platform","Contacts","Credits","Documentation","Downloads","How to configure","How to create a new plugin","How to monitor activities","How to restore the database","How to run","How to stop","Welcome to Ichnosat","Installation and Requirements","Introduction","src","Overview","Software architecture","src package","src.core package","src.core.downloader package","src.core.processing_pipe package","src.core.processing_pipe.scientific_processor package","src.core.processing_pipe.scientific_processor.src package","src.core.processing_pipe.src package","src.core.system_manager package","src.data package","src.data.database package","src.data.database.entities package","src.data.database.services package","src.data.logger package","src.presentation package","src.presentation.external_interface package","src.tests package","src.tests.downloader package","Tutorial"],titleterms:{"class":[7,17],"new":7,about:0,activ:[8,10],amazonbucketmanag:20,anatomi:[1,7],api:17,architectur:17,base:27,build:7,cli:25,code:[5,17],configur:[6,20],configurationmanag:20,consol:10,contact:2,content:[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],core:[19,20,21,22,23,24,25],creat:7,creation:7,credit:3,cron:6,data:[26,27,28,29,30],databas:[9,17,27,28,29],datasourc:20,declar:7,diagram:17,document:[4,17],download:[5,6,10,12,13,17,20,34],downloaderjob:20,each:6,entiti:28,exampl:7,extern:[7,17],external_interfac:32,file:6,folder:17,fork:12,github:12,global:6,graphic:6,gui:10,how:[6,7,8,9,10,11],ichnosat:[1,10,11,12],implement:7,index:12,init:25,instal:13,intefac:17,interfac:[6,7],interv:6,introduct:[6,7,14],job:24,jobdispatch:24,launch:10,librari:7,linux:13,log:10,logger:30,maco:13,manag:17,mani:6,method:7,modul:[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],monitor:[8,10],open:10,overview:[16,17],packag:[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],parallel:6,paramet:6,platform:[1,6],plugin:[7,24],pluginmanag:24,port:6,present:[31,32],process:[6,10],processing_pip:[21,22,23,24],processingpipemanag:24,processor:[6,7,17],product:[10,28],productdownload:20,products_servic:29,requir:13,restor:9,run:10,runner:33,schema:17,scientific_processor:[22,23],searchfilt:20,sens:6,sequenc:17,servic:29,set:6,skill:13,softwar:[13,17],sourc:5,src:[15,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],start:[23,32],stop:11,structur:17,submodul:[20,23,24,25,27,28,29,30,32,33,34],subpackag:[18,19,21,22,26,27,31,33],system:17,system_manag:25,technolog:17,test:[33,34],thread:6,tile:6,time:6,tutori:[4,35],user:6,via:10,welcom:12,work:7}})