import argparse
from posixpath import dirname
import sys
import os
import copy

import kolmogorov
import cyclomatic
import halstead
import potency

def main(argv):
    params  = parse_args(argv)
    
    src_list1,parentdir1 = scan_for_source_file(params.src)
    result1 = run_single_metrics(src_list1,parentdir1)

    if params.src2 != None:
        src_list2,parentdir2 = scan_for_source_file(params.src2)
        result2 = run_single_metrics(src_list2,parentdir2)
        
        filesource = True if parentdir2+parentdir1 == '' else False
        
        result_dual = run_dual_metrics(src_list1,src_list2,parentdir1,parentdir2,filesource)
        result = combine_result(result1,result2,filesource=filesource)
        result = combine_result(result,result_dual,srcflag=False,filesource=filesource)

        run_combined_metrics(result.files)
    else:
        result = result1

    html_output(result,params)
    os.startfile('html_out.html')
    #print_result(result)

def scan_for_source_file(src):
    '''
    src : file or directory path
    return
    ------
    list,string
        a list of source files and the top parent directory
    '''
    # only files with below extentions will be used
    allowed_sources = ['.py','.java']
    # check if file exist
    if not os.path.exists(src):
        raise RuntimeError("Given source file or directory doesn't exist")

    # if source is a single file return it in a list
    if os.path.isfile(src) and os.path.splitext(src)[1] in allowed_sources:
        return [src,],''
    # if source is a dir scan the dir to get all allowed
    # source files, sub dirs are also scanned.
    elif os.path.isdir(src):
        src = os.path.abspath(src)
        sources = []
        for dirpath,dirnames,filenames in os.walk(src):
            pdir = os.path.relpath(dirpath,src)
            for filename in filenames:
                if os.path.splitext(filename)[1] in allowed_sources:
                    sources.append(os.path.join(pdir,filename))
        return sources,src
    else:
        raise RuntimeError("invalid source")


def run_single_metrics(src_list,parentdir):
    '''
    result[
        {src:'source file',metric:''}
    ]
    '''
    result = ComplexityResult(parentdir)
    for src in src_list:
        file = os.path.join(parentdir,src)
        metrics = {}

        kolg = kolmogorov.calculate(file)
        cyclo = cyclomatic.calculate(file,True)
        hals = halstead.calculate(file,True)

        metrics['kolg'] = kolg[0]
        metrics['cyclo'] = cyclo[0]
        metrics['cyclo_avg'] = cyclo[1]
        metrics['hals'] = hals[0]
        
        file_result = result.add_file(src,metrics)

        file_result.add_function_results(cyclo[2],'cyclo')
        file_result.add_function_results(hals[1],'hals')

    return result

def run_dual_metrics(src_list1,src_list2,parentdir1,parentdir2,filesource=False):
    # getting common sources to a single list
    if filesource:
        parentdir1 = src_list1[0]
        parentdir2 = src_list2[0]
        src_list = ['']
    else:
        src_list = [ src for src in src_list1 if src in src_list2]
    result = ComplexityResult(parentdir1 +' & '+ parentdir2)
    for src in src_list:
        file1 = os.path.join(parentdir1,src).strip(os.sep)
        file2 = os.path.join(parentdir2,src).strip(os.sep)
        metrics = {}

        ami = kolmogorov.mutual_info(file1,file2)

        metrics['ami'] = ami[0]

        file_result = result.add_file(src,metrics)
    return result

def run_combined_metrics(result):
    for sub_result in result:
        for metrickey in sub_result.metrics:
            metric = sub_result.metrics[metrickey]
            if isinstance(metric,MultiResult):
                pot = potency.calculate(metric.result1,metric.result2)
                metric.combined['pot'] = pot
        if hasattr(sub_result,'functions'):
            run_combined_metrics(sub_result.functions)


def combine_result(result1,result2,srcflag=True,filesource=False):
    result1 = copy.deepcopy(result1)
    result2 = copy.deepcopy(result2)
    if filesource:
        result2.files[0].src = result1.files[0].src
    combine_sub_result(result1.files,result2.files,srcflag)
    result1.parent_dir = result1.parent_dir +' & '+ result2.parent_dir
    
    return result1

def combine_sub_result(sub_result1, sub_result2,srcflag):
    for result1 in sub_result1:
        match_found = False
        for result2 in sub_result2:
            if result1.src == result2.src:
                combine_result_metrics(result1.metrics,result2.metrics)

                if(hasattr(result2,'functions')):
                    combine_sub_result(result1.functions,result2.functions,srcflag)
                
                sub_result2.remove(result2)
                match_found = True
                break
        if srcflag and not match_found:
            result1.flags.add('src1-only')

    for result2 in sub_result2:
        if srcflag:
            result2.flags.add('src2-only')
        sub_result1.append(result2)

def combine_result_metrics(metrics1,metrics2):
    # combining metrics in metrics1 with same metrics
    # value from metric2.
    for metric in metrics1:
        if metric in metrics2:
            metrics1[metric] = MultiResult(metrics1[metric], metrics2[metric])
    # adding metrics that is only in metric2 to mmetric1
    for metric in metrics2:
        if metric not in metrics1:
            metrics1[metric] = metrics2[metric]


def html_output(result,params):
    src1 = os.path.abspath(params.src)
    src2 = None if params.src2 is None else os.path.abspath(params.src2)

    html_tail = ""
    with open(os.path.dirname(__file__) + os.path.sep +'html_output_tail.html','r') as f:
        html_tail = f.read()
    
    html = html_result_page(result,html_tail,src1,src2)

    with open('html_out.html','w') as f:
        f.write(html)

def html_result_page(result,tail,src1,src2):
    single_metrics_format = [
        {'h':"Kolmogorov",'k':'kolg','f':'{:.3f}','a':''},
        {'h':"Cyclomatic",'k':'cyclo','f':'{}','a':''},
        {'h':"avg.Cyclomatic",'k':'cyclo_avg','f':'{:.3f}','a':''},
        {'h':"Halstead",'k':'hals','f':'{}','a':''},
    ]
    dual_metrics_format = [
        {'h':"Algorithmic Mutual Information",'k':'ami','f':'{:.3f}','a':''},
    ]
    combined_metrics_format = [
        {'h':"Potency",'k':'pot','f':'{:.3f}','a':'class="potency"'},
    ]
    main_formats = single_metrics_format + dual_metrics_format
    sub_formats = combined_metrics_format

    html = '<html>'
    html += '<body>'
    html += '<h3>Source 1: '+src1+'</h3>'
    html += ('<h3>Source 2: '+src2+'</h3>') if src2 is not None else ''
    html += html_result_table(result,main_formats,sub_formats)
    html += '</body>'
    html += tail
    html += '</html>'
    return html

def html_result_table(result,main_formats,sub_formats,indent=1):
    indent1 = "\t" * indent
    indent2 = "\t" * (indent+1)
    indent3 = "\t" * (indent+2)
    indent4 = "\t" * (indent+3)

    html = indent1+"<table class='result'>"

    html += indent2+"<thead>"
    html += indent3+"<tr>"+indent4+"<th>Source</th>"+html_metrics_header_th(main_formats,indent+3)
    html += indent2+"</thead>"

    html += indent2+"<tbody>"
    for file_result in result.files:
        cls = 'src-file' + ' collapsed' if len(file_result.functions) > 0 else ''
        cls += ' '+' '.join(file_result.flags)
        html += indent3+'<tr class="'+cls+'">'
        html += indent4+'<td>'+file_result.src+'</td>'
        html += html_metrics_td(file_result.metrics,main_formats,sub_formats,indent+3)
        html += indent3+"</tr>"
        for func_result in file_result.functions:
            cls = 'src-func' + ' collapsed'
            cls += ' '+' '.join(func_result.flags)
            html += indent3+'<tr class="'+cls+'">'
            html += indent4+'<td>'+func_result.src+'@'+str(func_result.line)+'</td>'
            html += html_metrics_td(func_result.metrics,main_formats,sub_formats,indent+3)
            html += indent3+"</tr>"
    html += indent2+"</tbody>"

    html += indent1+"</table>"
    return html

def html_metrics_header_th(formats,indent=2):
    indent1 = "\t" * indent
    html = (indent1 + "<th>" +
            ("</th>"+indent1+"<th>").join(frt['h'] for frt in formats) +
            "</th>")
    return html

def html_metrics_td(metrics,main_formats,sub_formats,indent=4):
    indent1 = "\t" * indent
    html = ""
    for format in main_formats:
        key = format['k']
        attr = format['a']
        frt = format['f']
        html += indent1+"<td "+attr+">"

        if key in metrics:
            if isinstance(metrics[key],MultiResult):
                html += html_multiresult_table(metrics[key],format,sub_formats,indent+1)
            else:
                html += frt.format(metrics[key])

        html += "</td>"
    return html

def html_multiresult_table(multires,format,sub_formats,indent=5):
    indent1 = "\t" * indent
    indent2 = "\t" * (indent+1)
    indent3 = "\t" * (indent+2)
    frt = format['f']
    html = indent1+"<table>"
    html += indent2+("<tr>"+(indent3+"<td>"+frt+"</td>")*2+"</tr>").format(multires.result1,multires.result2)
    html += indent2+"<tr>" + html_metrics_td(multires.combined,sub_formats,[],indent+2) + "</tr>"
    html += indent1+"</table>"
    return html


class ComplexityResult:
    '''
    this stores result of complexity
    '''
    def __init__(self,pdir):
        self.parent_dir = pdir
        self.files = []
    
    def add_file(self,src,metrics):
        self.files.append(ComplexityFileResult(src,metrics))
        return self.files[-1]
    
class ComplexityFileResult:
    '''
    this is a class to store the result of running various metrics
    '''
    def __init__(self,src,metric=None):
        self.src = src
        self.metrics={}
        self.functions=[]
        self.flags = set()

        if metric is not None:
            self.metrics.update(metric)
    
    def add_function_results(self,func_list,metric):
        for func in func_list:
            self.add_function(func[0],func[1],{metric:func[2]})

    def add_function(self,src,line,metric):
        '''
        src : string
            function name
        line : int
            starting line number of function
        metric : dict
            {metric_name : metric_value, ...}
        '''
        func = self.find_function(src)
        if func:
            func.metrics.update(metric)
        else:
            func = ComplexityFuncResult(src,line,metric)
            self.functions.append(func)
    
    def find_function(self,src,line=None):
        '''
        src : string
            function name
        line : int (optional)
            function start line number
        
        return
        -------
        ComplexityFuncResult() 
            if given function found
         or
        None
            if given function not found
        '''
        for f in self.functions:
            if f.src == src and (line is None or f.line == line): 
                return f
        return None

class ComplexityFuncResult:
    '''
    this is a class to store result of functions
    '''

    def __init__(self,src,line,metric=None):
        self.src = src
        self.line = line
        self.metrics={}
        self.flags = set()

        if metric is not None:
            self.metrics.update(metric)

class MultiResult:
    '''
    used to store result when 2 results are combined
    '''
    def __init__(self,result1,result2):
        self.result1 = result1 
        self.result2 = result2 
        self.combined = {}

def parse_args(argv):
    description = ""
    parser = argparse.ArgumentParser(prog="main",description=description)

    parser.add_argument("src", type=str, action="store",
                        help="path of a source file or a directory containing multiple "+
                        "source files.")
    parser.add_argument("src2", type=str, action="store", default=None,nargs="?",
                        help="path of second source file or a directory containing multiple "+
                        "source files.")
    return parser.parse_args()

if __name__ == '__main__':
    #sys.argv.append('.\original_code.py')
    #sys.argv.append('.\embedded_code.py')
    #sys.argv.append('D:\\Python\\Amritha\\test\\t1\\original.py')
    #sys.argv.append('D:\\Python\\Amritha\\test\\t1\\embedded.py')

    sys.argv.append('complexity\\test\\t1\\embedded.py')
    sys.argv.append('complexity\\test\\t1\\embedded_salted3.py')
    main(sys.argv)
