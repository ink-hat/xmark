function evalPoly(poly,x)
{
    return poly.map((v,i) => { return v*Math.pow(x,i)}).reduce((t,v) => { return t+v },0)
}

function verifyPermPoly(poly,modulo)
{
    var yArray=[],y
    for(var i=0; i < modulo; i++)
    {
        y = evalPoly(poly,i) % modulo
        yArray.push(y)
    }
    console.log('values: '+yArray)
    console.log('sorted values: '+yArray.sort((a,b)=>{return a-b}))
    if(yArray.length == modulo)
    {
        dupli = yArray.filter((v,i,arr)=>{ return v == arr[i+1]})
        if(dupli.length > 0)
        {
            console.warn('Not perm poly duplicates: '+dupli)
        }
        else
            console.log('permutation poly')
    }
    else
        console.warn('not perm poly')
}