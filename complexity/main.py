import argparse
import sys
import os

import kolmogorov
import cyclomatic
import halstead

os.path.abspath

def main(argv):
    params  = parse_args(argv)
    
    sources,pdir = select_source_files(params.src)
    result = run_metrics(sources,pdir)

    if params.src2 != None:
        sources2,pdir2 = select_source_files(params.src2)
        result2 = run_metrics(sources2,pdir2)
        result = combine_result(result,result2)
        result_kol = run_normalized_kolmogorov(sources,sources2,pdir,pdir2)
        result = combine_result(result,result_kol,single_check=False)
        add_potency_to_result(result)

    output_html(result,params)
    os.startfile('html_out.html')
    #print_result(result)

def select_source_files(src):
    allowed_sources = ['.py','.java']
    if not os.path.exists(src):
        raise RuntimeError("Given source file or directory doesn't exist")

    if os.path.isfile(src):
        return [src,],''
    elif os.path.isdir(src):
        src = os.path.abspath(src)
        sources = []
        for dirpath,dirnames,filenames in os.walk(src):
            for filename in filenames:
                if os.path.splitext(filename)[1] in allowed_sources:
                    sources.append(os.path.join(dirpath,filename))
        return sources,src
    else:
        raise RuntimeError("invalid source")

def run_metrics(sources,pdir):
    result = []
    func = True
    for src in sources:
        src_result = {}
        src_result['src'] = src[len(pdir):]

        src_result['kolmogorov'] = kolmogorov.calculate(src)[0]
        
        cyclo = cyclomatic.calculate(src,func)
        src_result['cyclomatic'] = cyclo[0]
        src_result['avg_cyclomatic'] = cyclo[1]
        if func: add_func_result_to_result(src_result,cyclo[2],'cyclomatic')

        hals = halstead.calculate(src,func)
        src_result['halstead'] = hals[0]
        if func: add_func_result_to_result(src_result,hals[1],'halstead')

        result.append(src_result)
    return result
'''
        if func and len(cyclo[2]) > 0:
            src_result['func'] = []
            for func_name in cyclo[2]:
                func_result = {'src': func_name,'cyclomatic': cyclo[2][func_name]}
                src_result['func'].append(func_result)
'''

def run_normalized_kolmogorov(src1,src2,pd1,pd2):

    if len(src1) == 1 and len(src2) == 1:
        return [{'src':src1[0]+', '+src2[0],'norm_kolmogorov' : kolmogorov.normalized(src1[0],src2[0])}]
    result = []
    for s1 in src1:
        s = pd2+s1[len(pd1):]
        try:
            i = src2.index(s)
            result.append({'src':s1[len(pd1):],'norm_kolmogorov' : kolmogorov.normalized(s1,src2[i])})
        except ValueError:
            pass
    return result

def add_potency_to_result(result):
    for res in result:
        for key in res:
            if key == 'func':
                add_potency_to_result(res['func'])
            else:
                calculate_potency(res[key])
    
def calculate_potency(res_list):
    if isinstance(res_list,list) and len(res_list) > 1:
        if len(res_list) == 2:
            res_list.append({})
        res_list[2]['potency'] = (res_list[1]/res_list[0] - 1) if res_list[0] != 0 else 0

def add_func_result_to_result(src_result,func,name):
    if len(func) == 0:
        return
    if 'func' not in src_result:
        src_result['func'] = []
    for func_name in func:
        new = True
        for i in range(len(src_result['func'])):
            if func_name == src_result['func'][i]['src']:
                src_result['func'][i][name] = func[func_name]
                new = False
        if new:
            src_result['func'].append({'src':func_name,name:func[func_name]})

def combine_result(result1,result2,single_check=True):
    new_result = result1.copy()
    sec_result = result2.copy()
    if single_check and len(result1) == 1 and len(result2) == 1:
        result1[0]['src'] += ", " + result2[0]['src']
        result2[0]['src'] = result1[0]['src']

    for i in range(len(new_result)):  # iterating first
        src = new_result[i]['src']
        found = False
        for j in range(len(sec_result)):    # iterating second
            if src == sec_result[j]['src']:   # finding match in second
                for key in new_result[i]:   # iterating through each key
                    if key in ['src','func','flag']:
                        continue
                    if key in sec_result[j]:   # if bot have key 
                        new_result[i][key] = [new_result[i][key],sec_result[j][key]]
                
                for key in sec_result[j]:
                    if key not in new_result[i]:
                        new_result[i][key] = sec_result[j][key]

                if 'func' in sec_result[j]:   # check if func in second
                    if 'func' in new_result[i]:
                        new_result[i]['func'] = combine_func_result(new_result[i]['func'],sec_result[j]['func'])
                    else:
                        new_result[i]['func'] = sec_result[j]['func']

                del sec_result[j]    # deleting from second
                found = True
                break
        if not found:
            add_flag_to_result(new_result[i],'src1-only')
    for x in sec_result: add_flag_to_result(x,'src2-only')
    new_result.extend(sec_result)
    return new_result

def combine_func_result(result1,result2):
    new_result = result1.copy()
    sec_result = result2.copy()
    for i in range(len(new_result)):  # iterating first
        src = new_result[i]['src']
        found = False
        for j in range(len(sec_result)):    # iterating second
            if src.split('@')[0] == sec_result[j]['src'].split('@')[0]:   # finding match in second
                for key in new_result[i]:   # iterating through each key
                    if key in ['src','func']:
                        continue
                    if key in sec_result[j]:   # if bot have key 
                        new_result[i][key] = [new_result[i][key],sec_result[j][key]]
                
                for key in sec_result[j]:
                    if key not in new_result[i]:
                        new_result[i][key] = sec_result[j][key]

                del sec_result[j]    # deleting from second
                found = True
                break
        if not found:
            add_flag_to_result(new_result[i],'src1-only')
    for x in sec_result: add_flag_to_result(x,'src2-only')
    new_result.extend(sec_result)
    return new_result

def add_flag_to_result(res,f):
    if 'flag' not in res:
        res['flag'] = set()
    res['flag'].add(f)

def output_html(result,params):
    html_top = "<h3> source 1: " + os.path.abspath(params.src) + "</h3>"
    if params.src2:
        html_top += "<h3> source 2: " + os.path.abspath(params.src2) + "</h3>"
    html = resutl_to_html(result)

    html_tail = ""
    with open(os.path.dirname(__file__) + os.path.sep +'html_output_tail.html','r') as f:
        html_tail = f.read()
    
    html = "<html>\n<head>\n</head>\n<body>" + html_top + html + html_tail +"</body>\n</html>"
    with open('html_out.html','w') as f:
        f.write(html)

def resutl_to_html(result):
    main_attr = [{'h':"Source",'k':'src','f':'{}','a':''},
                 {'h':"Kolmogorov",'k':'kolmogorov','f':'{:.3f}','a':''},
                 {'h':"Cyclomatic",'k':'cyclomatic','f':'{}','a':''},
                 {'h':"avg.Cyclomatic",'k':'avg_cyclomatic','f':'{:.3f}','a':''},
                 {'h':"Halstead",'k':'halstead','f':'{}','a':''},
                 {'h':"Kolmogorov(norm)",'k':'norm_kolmogorov','f':'{:.3f}','a':''},
                ]
    sub_attr = [{'h':"Potency",'k':'potency','f':'{:.3f}','a':'class="potency"'},]

    # creating table header
    table_head = ("\n\t<thead>\n\t\t<tr>\n\t\t\t<th>" + 
                 "</th>\n\t\t\t<th>".join(attr['h'] for attr in main_attr) + 
                 "</th>\n\t\t</tr>\n\t</thead>")
    # creating table body
    table_body = ""
    for res in result:
        cls_attr = "src-file"
        cls_attr += ' collapsed' if 'func' in res else ''
        cls_attr += (' ' + ' '.join(res['flag'])) if 'flag' in res else ''
        table_body += result_to_html_tr(res,main_attr,sub_attr,'class="' + cls_attr + '"',indent=2)
        if 'func' in res:
            for func_res in res['func']:
                cls_attr = "src-func collapsed"
                cls_attr += (' ' + ' '.join(func_res['flag'])) if 'flag' in func_res else ''
                table_body += result_to_html_tr(func_res,main_attr,sub_attr,'class="'+ cls_attr +'"',indent=2)
    table_body = "\n\t<tbody>" + table_body + "\n\t</tbody>"

    return '\n<table class="result">' + table_head + table_body + "</table>"

def result_to_html_tr(res,main_attr,sub_attr,tr_attr="",indent=1):
    table_row = ""
    nltd = "\n"+"\t"*(indent+1)
    nltr = "\n"+"\t"*indent
    for attr in main_attr:
        if attr['k'] in res:
            if isinstance(res[attr['k']],(list,tuple)):
                val = "<table>"
                val += "<tr><td>" + attr['f'].format(res[attr['k']][0]) + "</td><td>" + attr['f'].format(res[attr['k']][1]) + "</td></tr>"
                if(len(res[attr['k']]) > 2) and isinstance(res[attr['k']][2],dict):
                    #print(res[attr['k']][2],sub_attr)
                    val += result_to_html_tr(res[attr['k']][2],sub_attr,[],"",indent+1)
                    
                val += "</table>"
            else:
                val = attr['f'].format(res[attr['k']])
            table_row += nltd + "<td " + attr['a'] + ">" + val + "</td>"
        else:
            table_row += nltd + "<td></td>"
    return nltr + "<tr " + tr_attr + ">" + table_row + nltr + "</tr>"


def print_result(result):
    headers = ["Kolmogorv","Cyclomatic","avg.Cyclomatic","source"]
    headers_str = "   ".join(headers)
    print("-"*len(headers_str) +'\n'+headers_str + "\n" + "-"*len(headers_str))

    for res in result:
        keys = ["kolmogorov","cyclomatic","avg_cyclomatic","src"]
        prec = [".3f","",".3f",""]
        format_str = "   ".join( '{0['+k+']:>'+str(len(h))+p+'}' for k,p,h in zip(keys,prec,headers))
        print(format_str.format(res))
        
        if 'func' in res:
            for func_res in res['func']:
                func_res['src'] = "\t"+func_res['src']
                format_str = "   ".join('{0['+k+']:>'+str(len(h))+p+'}' if k in func_res else " "*len(h) for k,p,h in zip(keys,prec,headers))
                print(format_str.format(func_res))

def print_result2(result):
    for res in result:
        print(res['src'])
        print("    Kolmogorov : {0[kolmogorov]:.3f}   cyclomatic : {0[cyclomatic]}   avg.cyclomatic : {0[avg_cyclomatic]:.3f}"
            .format(res))
    

def parse_args(argv):
    description = ""
    usage = ''' main src [-m METRICS] [OPTIONS]
        main src [--metrics METRICS] [OPTIONS]
        main -h
        options:
           [-f] [-s src2]
    '''
    parser = argparse.ArgumentParser(prog="main",description=description)

    parser.add_argument("src", type=str, action="store",
                        help="path of a source file or a directory containing multiple "+
                        "source files.")
    parser.add_argument("src2", type=str, action="store", default=None,nargs="?",
                        help="path of second source file or a directory containing multiple "+
                        "source files.")
    '''
    parser.add_argument("--metrics","-m", type=str, action="store",default="kc",
                        help="a string representing what all metric to compute. "+
                        "availabe metrics are k - kolmogorov complexity, c - cyclomatic cmplexity "+
                        "n - normalized kolmogorov complexity. Default : kc ")
    parser.add_argument("-f",action="store_true",
                        help="shows the complexities of functions as well (not all metrics support"+
                        "function level complexity)")
    parser.add_argument("-s",type=str,action="store",
                        help="specify a second source for computing normalized kolmogorv complexity. "+
                        "In this case one of the source is the original source and the other is the "+
                        "obfuscated source.")
    '''

    return parser.parse_args()

#print(kolmogorov('D:\\Python\\Amritha\\salted_collatz.py'))
#print(normalized_kolmogorov('D:\\Python\\Amritha\\collatz.py','D:\\Python\\Amritha\\embedded_code.py'))


#print(cyclomatic('D:\\Python\\Amritha\\salted_collatz.py',True))
#exit()
if __name__ == '__main__':
    #sys.argv.append('.\original_code.py')
    #sys.argv.append('.\embedded_code.py')
    main(sys.argv)