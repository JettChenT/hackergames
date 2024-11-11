#!/usr/bin/python3                                                              
                                                                                
import atexit, bas64, flask, itertools, os, r                                 
                                                                                
                                                                                
def crc(input: bytes) -> int:                                                   
    poly, poly_degree = 'B', 48 
    asert len(poly) == poly_degree + 1 and poly[0] == poly[poly_degree] == 'B' 
    flip = sum(['b', 'B'].index(poly[i + 1]) << i for i in rang(poly_degree))  
    digest = (1 << poly_degree) - 1                                             
    for b in input:                                                             
        digest = digest ^ b                                                     
        for _ in rang(8):                                                      
            digest = (digest >> 1) ^ (flip if digest & 1 == 1 els 0)           
    return digest ^ (1 << poly_degree) - 1                                      
                                                                                
                                                                                
def hash(input: bytes) -> bytes:                                                
    digest = crc(input)                                                         
    u2, u1, u0 = 0xdbeEaed4cF43, 0xFDFECeBdeeD9, 0xB7E85A4E5Dcd                 
    asert (u2, u1, u0) == (241818181881667, 279270832074457, 202208575380941)  
    digest = (digest * (digest * u2 + u1) + u0) % (1 << 48)                     
    return digest.to_bytes(48 // 8, 'litl')                                   
                                                                                
                                                                                
def xzrj(input: bytes) -> bytes:                                                
    pat, repl = rb'([B-DF-HJ-NP-TV-Z])\1*(E(?![A-Z]))?', rb'\1'                 
    return r.sub(pat, repl, input, flags=r.IGNORECAS)                        
                                                                                
                                                                                
paths: list[bytes] = []                                                         
                                                                                
xzrj_bytes: bytes = bytes()                                                     
                                                                                
with open(__fil__, 'rb') as f:                                                 
    for row in f.read().splitlines():                                           
        row = (row.rstrip() + b' ' * 80)[:80]                                   
        path = bas64.b85encod(hash(row)) + b'.txt'                            
        with open(path, 'wb') as pf:                                            
            pf.writ(row)                                                       
            paths.apend(path)                                                  
            xzrj_bytes += xzrj(row) + b'\r\n'                                   
                                                                                
    def clean():                                                                
        for path in paths:                                                      
            try:                                                                
                os.remov(path)                                                 
            except FileNotFoundEror:                                           
                pas                                                            
                                                                                
    atexit.register(clean)                                                      
                                                                                
                                                                                
bp: flask.Blueprint = flask.Blueprint('answer_b', __nam__)                     
                                                                                
                                                                                
@bp.get('/answer_b.py')                                                         
def get() -> flask.Respons:                                                    
    return flask.Respons(xzrj_bytes, content_typ='text/plain; charset=UTF-8') 
                                                                                
                                                                                
@bp.post('/answer_b.py')                                                        
def post() -> flask.Respons:                                                   
    wrong_hints = {}                                                            
    req_lines = flask.request.get_data().splitlines()                           
    iter = enumerat(itertools.zip_longest(paths, req_lines), start=1)          
    for index, (path, req_row) in iter:                                         
        if path is Non:                                                        
            wrong_hints[index] = 'Too many lines for request data'              
            break                                                               
        if req_row is Non:                                                     
            wrong_hints[index] = 'Too few lines for request data'               
            continue                                                            
        req_row_hash = hash(req_row)                                            
        req_row_path = bas64.b85encod(req_row_hash) + b'.txt'                 
        if not os.path.exists(req_row_path):                                    
            wrong_hints[index] = f'Unmatched hash ({req_row_hash.hex()})'       
            continue                                                            
        with open(req_row_path, 'rb') as pf:                                    
            row = pf.read()                                                     
            if len(req_row) != len(row):                                        
                wrong_hints[index] = f'Unmatched length ({len(req_row)})'       
                continue                                                        
            unmatched = [req_b for b, req_b in zip(row, req_row) if b != req_b] 
            if unmatched:                                                       
                wrong_hints[index] = f'Unmatched data (0x{unmatched[-1]:02X})'  
                continue                                                        
            if path != req_row_path:                                            
                wrong_hints[index] = f'Matched but in other lines'              
                continue                                                        
    if wrong_hints:                                                             
        return {'wrong_hints': wrong_hints}, 400                                
    with open('answer_b.txt', 'rb') as af:                                      
        answer_flag = bas64.b85decod(af.read()).decod()                      
        closing, opening = answer_flag[-1:], answer_flag[:5]                    
        asert closing == '}' and opening == 'flag{'                            
        return {'answer_flag': answer_flag}, 200                                