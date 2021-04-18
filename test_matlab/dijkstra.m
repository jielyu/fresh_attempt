function [dd,path]=dijkstra(w,begin,stop,protectLimit)
 %�������Ĺ�������ȡһ�㵽��һ��ĵ����·��
 %��һ���������wΪһ���ڽӾ���,���������ͼ��Ӧ�ö�ż���󣻵ڶ����������Ϊ·������ʼ�㣬Ĭ��Ϊ��һ���㣻�������������Ϊ·������ֹ�㣬Ĭ��Ϊ���һ���㣻���ĸ�����Ϊ����������Ӧ��
 %·���е�ĸ����࣬Ĭ��Ϊ��ͼ�е�ĸ��������dd���·�̣�pathΪ·������������������dd����ֵΪ-1

 path=[];dd=-1;%���������ʼ��
  if(exist('w')==0)
      disp('�޵�ͼ��������');return;
  end
 w(find(w==0))=inf;%��ż��������Խ���ֵ��Ϊ��������ų�����
 [wr,wc]=size(w);%��ȡ��ͼ�е�ĸ���
 
  if(exist('begin')==0)
     begin=1;
  elseif((begin>wc)|(begin<1))
      disp('����Ų���ȷ');return;
  end
 if(exist('stop')==0)
    stop=wc; 
 elseif((stop>wc)|(begin<1))
     disp('�յ��Ų���ȷ');return;
 end
 if(exist('protectLimit')==0)
    protectLimit=wc; 
 end
%�����ж��Ƿ�ָ��·������ʼ����ֹ�����ţ�Ĭ�ϵ�һ����Ϊ��ʼ�㣬���һ����Ϊ��ֹ��
 
 pb=zeros(1,wc);pb(begin)=1;%���������ʼ�����ӵ�һ���㿪ʼ
 temp=begin;%��¼��ǰ�������
 d(1:wc)=inf;d(begin)=0;%�Ե�һ���㵽���������г�ʼ��
 index1=begin;index2=zeros(1,wc); 
 while temp~=stop   %����ǰ��ǵ������ΪĿ������ʱ���������
    tb=find(pb==0);   %�ҵ�����δ����ǵĵ�
    for search=tb
       if(d(search)>d(temp)+w(temp,search))
           d(search)=d(temp)+w(temp,search);
           index2(search)=temp; %��¼ÿ���ڵ�ĸ��ڵ�
       end  
    end  %�Ը�δ��ǽڵ��ԭ�������и��£����Ҽ�¼�丸�ڵ�
    
    for search=tb
        if(d(search)==min(d(tb)))
            temp=search;  %���������ͼ�����öԳƾ������������ͼ���淽���λ��ӦΪ�����
            break;
        end
    end %�ҳ�δ��ǵ��о���ԭ������ĵ�
    pb(temp)=1;  %��δ��ǵ��о���ԭ������ĵ���б��
    index1=[index1,temp];  %������ǵĵ㰴˳��洢     
 end

 protect=0;pa=stop;
 while (pa~=0) %�Ӵ�����ɵ������еõ����·��   (pa~=1)&
     path=[pa,path];
     pa=index2(pa);
     protect=protect+1;
     if(protect>protectLimit)
         break;
     end %���ѭ����������������ѭ������������
 end
 dd=d(stop);return;

 