function [dd,path]=dijkstra(w,begin,stop,protectLimit)
 %本函数的功能是求取一点到另一点的的最短路径
 %第一个输入参数w为一个邻接矩阵,如果是无向图，应用对偶矩阵；第二个输入参数为路径的起始点，默认为第一个点；第三个输入参数为路径的终止点，默认为最后一个点；第四个参数为保护参数，应比
 %路径中点的个数多，默认为地图中点的个数；输出dd最短路程，path为路径，如果输入参数有误，dd返回值为-1

 path=[];dd=-1;%输出变量初始化
  if(exist('w')==0)
      disp('无地图数据输入');return;
  end
 w(find(w==0))=inf;%对偶矩阵的主对角线值设为无穷大，以排除干扰
 [wr,wc]=size(w);%获取地图中点的个数
 
  if(exist('begin')==0)
     begin=1;
  elseif((begin>wc)|(begin<1))
      disp('起点编号不正确');return;
  end
 if(exist('stop')==0)
    stop=wc; 
 elseif((stop>wc)|(begin<1))
     disp('终点编号不正确');return;
 end
 if(exist('protectLimit')==0)
    protectLimit=wc; 
 end
%用于判断是否指定路径的起始和终止点的序号，默认第一个点为起始点，左后一个点为终止点
 
 pb=zeros(1,wc);pb(begin)=1;%标记向量初始化，从第一个点开始
 temp=begin;%记录当前点的索引
 d(1:wc)=inf;d(begin)=0;%对第一个点到各点距离进行初始化
 index1=begin;index2=zeros(1,wc); 
 while temp~=stop   %当当前标记点的索引为目标索引时，处理结束
    tb=find(pb==0);   %找到所有未被标记的点
    for search=tb
       if(d(search)>d(temp)+w(temp,search))
           d(search)=d(temp)+w(temp,search);
           index2(search)=temp; %记录每个节点的父节点
       end  
    end  %对各未标记节点距原点距离进行更新，并且记录其父节点
    
    for search=tb
        if(d(search)==min(d(tb)))
            temp=search;  %如果是无向图，需用对称矩阵，如果是有向图，逆方向的位置应为无穷大
            break;
        end
    end %找出未标记点中距离原点最近的点
    pb(temp)=1;  %对未标记点中距离原点最近的点进行标记
    index1=[index1,temp];  %将做标记的点按顺序存储     
 end

 protect=0;pa=stop;
 while (pa~=0) %从处理完成的数据中得到最短路径   (pa~=1)&
     path=[pa,path];
     pa=index2(pa);
     protect=protect+1;
     if(protect>protectLimit)
         break;
     end %如果循环次数过多则跳出循环，保护程序
 end
 dd=d(stop);return;

 