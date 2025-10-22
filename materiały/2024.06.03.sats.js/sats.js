/*
  Demonstracja działania algorytmów:
   - symulowane wyżarzanie (SA)
   - poszukoiwanie z zabronieniami (TS)
  na problemie komiwojażera (TSP)
  M.Makuchowski
*/

const nodeN=40;           // liczba miast
var node=[];              // dane instancji

var saPath=[];            // sa: ścieżka
var saDataDist=[];        // sa: dane wykresu Dist
var saBestDist;           // sa: najlepsze znalezione Dist
var saBestPath;           // sa: najlepsze znaleziona ścieżka
var saTempStart=10000;    // sa: temperatura Startowa
var saTempAlpha=0.976;    // sa: współczynnik zmiany temperatury
var saTemp;               // sa: temperatura

var tsPath=[];            // ts: ścieżka
var tsDataDist=[];        // ts: dane wykresu Dist
var tsBestDist;           // ts: najlepsze znalezione Dist
var tsBestPath;           // ts: najlepsze znaleziona ścieżka
var tsTabu=[];            // ts: listaTabu
var tsTabuSize=32;        // ts: ilosc elementów na liscie tabu

var loopN=0;              // ile pozostalo kroków do wykonania
var loopDelay=10;         // opoźnienie pętli

////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
////                                                    ////
////  Główna pętla programu                             ////
////                                                    ////
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////

function Run()
{
  var startPath=RandPath();
  var startDist=PathDist(startPath);
  saPath=Array.from(startPath);
  tsPath=Array.from(startPath);
  saDataDist=[]; saDataDist.push(startDist);
  tsDataDist=[]; tsDataDist.push(startDist);
  saBestDist=startDist; saBestPath=Array.from(startPath);
  tsBestDist=startDist; tsBestPath=Array.from(startPath);

  tsTabu=[];
  isRun=1;
  loopN=400;
  saTemp=saTempStart;
  Loop();
}

function Loop()
{
  if(loopN==0)return;
  loopN--;
  SaStep( saPath,saTemp ) ;
  TsStep( tsPath ) ;
  saTemp = saTemp*saTempAlpha;
  saDataDist.push( PathDist( saPath ));
  tsDataDist.push( PathDist( tsPath ));
  if(loopN==0)
  {
    saPath=saBestPath;
    tsPath=tsBestPath;
    saDataDist.push(saBestDist);
    tsDataDist.push(tsBestDist);
  }
  Draw();
  setTimeout(Loop,loopDelay);
}

//////////////////////////////////////////////////////////////
//                         SA                               //
//////////////////////////////////////////////////////////////
function SaStep(path,temp)
{
  var c0 = PathDist(path);
  var praw=0,akce=0;
  //tyle samo iteracji w 1 krok co algorytm TS
  var N= (node.length-1)*(node.length-2)/2;
  for(var i=0; i<N; i++)
  {
    var move = RandAB();
    PathMove( path,move );
    var c1 = PathDist(path);
    if(c1>c0)
    { praw = Math.exp( (c0-c1)/temp );
      akce = ( Math.random()<praw );
    }
    if(c1<=c0||akce)  c0=c1; //akceptuje ruch
    else     PathMove( path,move ); //odrzucenie ruchu
    if(saBestDist>c0)
    {
      saBestDist=c0;
      saBestPath=Array.from( path );
    }
  }
}

//////////////////////////////////////////////////////////////
//                         TS                               //
//////////////////////////////////////////////////////////////

function TsStep(path)
{
  var move = TsFindBestMove( path );
  TsAddMoveTabu( path,move );
  PathMove( path,move );
}

function TsFindBestMove(path)
{
  var bestA=0,bestB=0,bestDist=999999999;
  for(a=1;a<node.length-1;a++)
    for(b=a+1;b<node.length;b++)
    {
      PathMove(path,[a,b]);
      var Dist=PathDist(path);

      if(TsIsPathTabu(path)==0 && Dist<bestDist )
        {bestA=a;bestB=b;bestDist=Dist;}

      if(Dist<tsBestDist)
        {bestA=a;bestB=b;bestDist=Dist;}

      if(tsBestDist>bestDist)
        { tsBestDist=bestDist; tsBestPath=Array.from( path ); }

      PathMove(path,[a,b]);
    }
  return [bestA,bestB];
}

function TsIsPathTabu(path)
{
  for(i=0; i<tsTabu.length; i++)
    if( path[tsTabu[i][0]]==tsTabu[i][1] ) return 1;
  return 0;
}

function TsAddMoveTabu( path,move )
{
  var a=move[0];
  var b=move[1];
  if((a==0)&&(b==0)) {tsTabu.splice(0,2); return;}
  tsTabu.push( [a,path[a]] );
  tsTabu.push( [b,path[b]] );
  if(tsTabu.length>(2*tsTabuSize)) tsTabu.splice(0,2);
}

//////////////////////////////////////////////////////////////
// inne                                                     //
//////////////////////////////////////////////////////////////
function NodeRand()
{
  node=[]; saPath=[]; tsPath=[];
  saDataDist=[]; tsDataDist=[];
  for(i=0;i<nodeN;i++)
    node.push([ Math.floor(Math.random()*400), Math.floor(Math.random()*200)]);
  Draw();
}

function RandAB()
{
  //Losowa paraliczb (od 1)
  var a=1+Math.floor(Math.random()*(node.length-1));
  var b=1+Math.floor(Math.random()*(node.length-2)); if(b>=a)b++;
  if(a>b) [a,b]=[b,a];
  return [a,b];
}

function RandPath()
{
  //losowa permutacja zaczynająca się od zera
  var path=[];
  for( i=0; i<node.length; i++) path.push(i);
  for (let i = path.length - 1; i > 0; i--)
  { const j = Math.floor(Math.random()*i+1 );
    [path[i], path[j]] = [path[j], path[i]];
  }
  return path;
}

function PathMove(path,move)
{
  var a=move[0], b=move[1];
  while(a<b){[path[a],path[b]]=[path[b],path[a]]; a++;b--;}
  //[path[a],path[b]]=[path[b],path[a]];
}

function PathDist(path)
{
  var dist=0;
  for(var i=0; i<path.length; i++)
  { var n0 = path[i];
    var n1 = path[(i+1)%path.length];
    var x0 = node[n0][0];
    var y0 = node[n0][1];
    var x1 = node[n1][0];
    var y1 = node[n1][1];
    dist += Math.round(Math.sqrt((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1)));
  }
  return dist;
}

///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
////                                                  /////
////  Grafika                                         /////
////                                                  /////
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////

function NodeXY(id)
{
  var scale=   1;
  var shiftX=  20;
  var shiftY=  20;
  return [ shiftX+scale*node[id][0], shiftY+scale*node[id][1] ];
}
function SvgKrata()
{
  svg="";
  svg+='<g style="stroke: #242424; stroke-width:1; fill: none;">';
  svg+='<path d="M 20 20';
  for(var i=0;i<25;i++)svg+='m -10 0, l 420 0, m -410 8';
  svg+='M 20 20';
  for(var i=0;i<50;i++)svg+='m 0 -10, l 0 220, m 8 -210';
  svg+='"/></g>';

  svg+='<g style="stroke: #2e2e2e; stroke-width:1; fill: none;">';
  svg+='<path d="M 20 20';
  for(var i=0;i<=5;i++)svg+='m -10 0, l 420 0, m -410 40';
  svg+='M 20 20';
  for(var i=0;i<=10;i++)svg+='m 0 -10, l 0 220, m 40 -210';
  svg+='"/></g>';

  return svg;
}

function SvgPath(path)
{
  var svg = '<svg width="440" height="240">';
  svg+=SvgKrata();
  if(path.length>0)
  { //Path
    svg+='<g style="stroke: #cc7; stroke-width:3; fill: none; stroke-linejoin:bevel ">';
    var x,y; [x,y] = NodeXY(path[0]);
    svg+='<path d="M '+x+' '+y;
    for(var i=1; i<path.length; i++ )
    { [x,y]= NodeXY(path[i]);
      svg+=', L '+x+' '+y;
    } svg+=',Z"/></g>';
  }
  //Node
  for(var i=0; i<node.length; i++ )
  { [x,y]= NodeXY(i);
    svg+='<circle cx="'+x+'" cy="'+y
       +'" r="4" stroke=#none fill=#474 />'
  }
  svg+='</svg>';
  return svg;
}

function SvgDataDist(data)
{
  var svg= '<svg width="440" height="240">';
  svg+=SvgKrata();
  svg+='<line x1="10" y1="220" x2="430" y2="220" style="stroke:#777;stroke-width:1" />';
  svg+='<line x1="20" y1="230" x2="20"  y2="10" style="stroke:#777;stroke-width:1" />';

  if(data.length>0){
    var scala = 160/data[0];
    svg+='<g style="stroke: #cc7; stroke-width:2; fill: none;">';
    svg+='<path d="M 20 60';
    for(var i=1;i<data.length;i++)
      svg+=',L '+(20+i)+' '+(220-scala*data[i]);
    svg+='"/></g>';
    svg+='<text x="350" y="35" fill="#777" font-size="16" >'+
          +(data[data.length-1])+'</text>';
  }
  svg+='</svg>';
  return svg;
}

function Draw()
{
  document.getElementById("saPathSvg").innerHTML=SvgPath(saPath);
  document.getElementById("saDistSvg").innerHTML=SvgDataDist(saDataDist);
  document.getElementById("tsPathSvg").innerHTML=SvgPath(tsPath);
  document.getElementById("tsDistSvg").innerHTML=SvgDataDist(tsDataDist);
}

///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
////                                                  /////
////  Start strony                                    /////
////                                                  /////
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////

function Init()
{
  document.onselectstart = function(){return false;};
  document.getElementById('rand').addEventListener('click',NodeRand);
  document.getElementById('run').addEventListener('click',Run);
  document.getElementById('saPath').innerHTML= '<div id="saPathTxt">SA: ścieżka</div> <div id="saPathSvg">path:svg</div>';
  document.getElementById('saDist').innerHTML= '<div id="saDistTxt">SA: długość</div> <div id="saDistSvg">Dist:svg</div>';
  document.getElementById('tsPath').innerHTML= '<div id="tsPathTxt">TS: ścieżka</div> <div id="tsPathSvg">path:svg</div>';
  document.getElementById('tsDist').innerHTML= '<div id="tsDistTxt">TS: długość</div> <div id="tsDistSvg">Dist:svg</div>';
  NodeRand();
}

Init();
