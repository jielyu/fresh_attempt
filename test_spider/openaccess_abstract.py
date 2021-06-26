# encoding: utf-8

import os, sys, time
import requests
import bs4
import pickle
import uuid
import argparse

class CvfHtmlAbstract(object):

    def __init__(self):
        pass

    @staticmethod
    def getTimeStamp():
        """
        Function: Get string of current time stamp
        Input:
            None
        Output:
            string, time stamp
        Date: 2018-04-24
        Author: Jie Lyu
        """
        t = time.localtime(time.time())
        t_str = time.strftime('%Y-%m-%d-%H-%M-%S', t)
        return t_str

    def getTextStr(self, html_path):
        if not os.path.isfile(html_path):
            try:
                response = requests.get(html_path)
                html_str = response.text
            except requests.RequestException:
                print('Warning: fail to request url={}'.format(html_path))
                html_str = None
            return html_str
        else:
            with open(html_path) as fid:
                html_str = fid.read()
            return html_str

    def parseOpenAccessPage(self, oa_str):
        # Construct DOM 
        soup = bs4.BeautifulSoup(oa_str)
        title_list = soup.select('dt a')
        # Extract all relative links of papers
        href_list = []
        for elem in title_list:
            href = elem['href']
            href_list.append(href)
        return href_list

    def parseCvfPage(self, cvf_str):
        # Construct DOM
        soup = bs4.BeautifulSoup(cvf_str)
        # Extract title, authos and abstrct
        try:
            title = soup.select('#papertitle')[0].string.strip()
            authors = soup.select('#authors i')[0].string.strip()
            abstract = soup.select('#abstract')[0].string.strip()
        except IndexError:
            title, authors, abstract = ' ', ' ', ' '
        # Return
        return title, authors, abstract

    def extract(self, html_url, md_path, name='Abstract Collection'):
        if os.path.isfile(md_path):
            print('Info:{}, generated file: {}'.format(self.getTimeStamp(), md_path))
        else:
            # Create tmp directory
            # tmp_dir = '%s'%(uuid.uuid4())
            tmp_dir = '.tmp_%s'%(name)
            if not os.path.isdir(tmp_dir):
                os.makedirs(tmp_dir)
            tmp_path_list = []
            # Get content of open access page
            oa_str = self.getTextStr(html_path=html_url)
            # Get relative links of all papers
            oa_str.encode('UTF-8', 'ignore')
            href_list = self.parseOpenAccessPage(oa_str)
            # Visit each paper page
            base_link = os.path.dirname(html_url)
            for idx,href in enumerate(href_list):
                tmp_pkl_path = os.path.join(tmp_dir, '%0*d.pkl'%(5, idx))
                tmp_path_list.append(tmp_pkl_path)
                if not os.path.isfile(tmp_pkl_path):
                    # Generate url for each paper page
                    cvf_paper_url = base_link + '/' + href
                    # Get content of paper page
                    cvf_str = self.getTextStr(html_path=cvf_paper_url)
                    # Get title, authors, abstract
                    title, authors, abstract = self.parseCvfPage(cvf_str=cvf_str)
                    tmp_dict = {'title':title, 'authors':authors, 'abstract':abstract}
                    print('Info:{}, idx={} succ'.format(self.getTimeStamp(), idx))
                    #print(u'Info:{}, idx={}, title={}'.format(self.getTimeStamp(), idx, title))
                    # Write into pkl file
                    with open(tmp_pkl_path, 'wb') as fid:
                        pickle.dump(tmp_dict, fid)
            # Write into md file
            self.mergeToMarkdown(pkl_path_list=tmp_path_list, md_path=md_path, name=name)

    def mergeToMarkdown(self, pkl_path_list, md_path, name='Abstract Collection'):
        if not os.path.isfile(md_path):
            with open(md_path, 'w') as fid:
                md_str = '# ' + name + '\r\n'
                fid.write(md_str)
                tmp_dir = os.path.dirname(pkl_path_list[0])
                for idx, pkl_path in enumerate(pkl_path_list):
                    with open(pkl_path, 'rb') as pkl:
                        tmp_dict = pickle.load(pkl)
                    id = '%d. '%(idx+1)
                    md_str = '### ' + id + tmp_dict['title'] + '\r\n'
                    # print(md_str)
                    md_str = md_str + '*' + tmp_dict['authors'] + '*\r\n'
                    md_str = md_str + '***Abstract:*** ' + tmp_dict['abstract'] + '\r\n'
                    fid.write(md_str.encode('utf-8')) 
                    # Remove tmp files
                    os.remove(pkl_path)
                # Remove tmp directory
                os.rmdir(tmp_dir)
                
            print('Info:{}, generated file: {}'.format(self.getTimeStamp(), md_path))
        else:
            print('Warning: exist output file: {}'.format(md_path))


def extract_conf(html_url, dst_dir='./output', name='Abstract Collection'):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    md_path = os.path.join(dst_dir, name+'.md')
    cvf_ext = CvfHtmlAbstract()
    cvf_ext.extract(html_url=html_url, md_path=md_path, name=name)
    return md_path

NAME_URL_DICT = {}
NAME_URL_DICT['cvpr2018'] = ['http://openaccess.thecvf.com/CVPR2018.py', 'CVPR2018-Abstract-Collection']
NAME_URL_DICT['cvpr2017'] = ['http://openaccess.thecvf.com/CVPR2017.py', 'CVPR2017-Abstract-Collection']
NAME_URL_DICT['cvpr2016'] = ['https://www.cv-foundation.org/openaccess/CVPR2016.py', 'CVPR2016-Abstract-Collection']
NAME_URL_DICT['cvpr2015'] = ['https://www.cv-foundation.org/openaccess/CVPR2015.py', 'CVPR2015-Abstract-Collection']
NAME_URL_DICT['cvpr2014'] = ['http://openaccess.thecvf.com/CVPR2014.py', 'CVPR2014-Abstract-Collection']
NAME_URL_DICT['cvpr2013'] = ['https://www.cv-foundation.org/openaccess/CVPR2013.py', 'CVPR2013-Abstract-Collection']
NAME_URL_DICT['iccv2017'] = ['http://openaccess.thecvf.com/ICCV2017.py', 'ICCV2017-Abstract-Collection']
NAME_URL_DICT['iccv2015'] = ['https://www.cv-foundation.org/openaccess/ICCV2015.py', 'ICCV2015-Abstract-Collection']
NAME_URL_DICT['iccv2013'] = ['http://openaccess.thecvf.com/ICCV2013.py', 'ICCV2013-Abstract-Collection']
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of conference')
    args = parser.parse_args()
    name = args.name.lower()
    if name in NAME_URL_DICT:
        print('url={}, name={}'.format(NAME_URL_DICT[name][0], NAME_URL_DICT[name][1]))
        md_path = extract_conf(html_url=NAME_URL_DICT[name][0], name=NAME_URL_DICT[name][1])
        print('extract abstrcts finished, result in file:{}'.format(md_path))
    else:
        print('available name listed as follow:')
        for key in NAME_URL_DICT:
            print(key + ','),


if __name__ == '__main__':
    main()