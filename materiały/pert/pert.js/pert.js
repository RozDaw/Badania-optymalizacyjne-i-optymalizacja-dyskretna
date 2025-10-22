///////////////////////////////////////////////////////////
////                                                  /////
////  Interakcja strony PERT                          /////
////                                                  /////
///////////////////////////////////////////////////////////

class Gauss
{
  avg=0;
  sig=1;

  Scale(x)
  {
    x = x-this.avg;
    x = x/this.sig;
    return x;
  }
  ScaleInv(x)
  {
    x = x*this.sig;
    x = x+this.avg;
    return x;
  }


  Cdf(x)
  {
    let sgn=(x>0)-(x<0);
    let t=1.0/(1+0.2316418883*sgn*x);
    let  w=+0.254829592*t -0.284496736*t*t +1.421413741*t*t*t
             -1.453152027*t*t*t*t +1.061405429*t*t*t*t*t;
    return 0.5*(1+sgn*(1.0-w*Math.exp(-x*x/2.0)));
  }

  CdfInv(x)
  {
    var sgn=(x>0.5)-(x<0.5);
    var lnx=Math.log(4.0*x-4.0*x*x), tmp=(4.330746751+0.5*lnx);
    var y=sgn*Math.sqrt(2*(Math.sqrt(tmp*tmp-6.802721088*lnx)-tmp));
    tmp=this.Cdf(y); y=y+(x-tmp)*0.001/(this.Cdf(y+0.001)-tmp); //można x2
    return y;
  }

}

const  gauss=new Gauss();

class GraphXY
{ // klasa GRAFU z nodes[]{x,y} edges[]{a,b}//
  nodes=[];
  edges=[];

  SetNodesRand(nodeN,xMax,yMax,dMin)
  { //losuje wierzchołki//
    //  nodeN:  liczba wierzchołków,
    //  xyMax:  zakres wspołrzędnych 0<= xy <xyMax,
    //  dMin:   minimalna odległość między wierzchołkami > dMin
    this.nodes=[];
    //losowanie aż do pełnej listy node ale nie więcej niż 4nodeN
    for(let i=0,k=0;i<nodeN;)
    { //losowanie x,y
      let [x,y]= [ xMax*Math.random(), yMax*Math.random() ];
          [x,y]= [ Math.round(x),Math.round(y) ];
      //dopisywanie
      if(this.#IsSpace([x,y],dMin))
        {i++;this.nodes.push({x:x,y:y});}
      //zabezpieczenie: robi reset pętli
      k=k+1; if(k>nodeN*4){k=0;i=0;this.nodes=[];}
    }
    { //pseudo skalowanie do min max
      let id1=0,id2=0,id3=0,id4=0;
      for(let i=0;i<this.nodes.length;i++)
      { if(this.nodes[i].x<this.nodes[id1].x)id1=i;
        if(this.nodes[i].y<this.nodes[id2].y)id2=i;
        if(this.nodes[i].x>this.nodes[id3].x)id3=i;
        if(this.nodes[i].y>this.nodes[id4].y)id4=i;
      }
      this.nodes[id1].x=0;
      this.nodes[id2].y=0;
      this.nodes[id3].x=xMax;
      this.nodes[id4].y=yMax;
    }
  }

  SetEdges(nodeDist,alfa)
  { //tworzy zbiór ładnych krawędzi://
    // - nieprzecinających się
    // - przebiegających z daleka od wierzchołków
    // - tworzących z innymi krawędziami duże kąty (kąt>alfa)
    let cos  = Math.cos(alfa*2*3.1415/360);
    { //tworze zbiór krawędzi edgesSort:
      //wszystkie krawędzie posortowane od najkrótszej
      var edgesSort=[];
      for(let a=0;a<this.nodes.length;a++)
        for(let b=a+1;b<this.nodes.length;b++)
          edgesSort.push({a:a,b:b,dXY:this.#Distance_2id(a,b)});
      edgesSort.sort((u,v)=>(u.dXY>v.dXY)?1:-1 );
    }

    { //tworze zbiór krawędzi edges:
      this.edges=[];
      for(let i=0;i<edgesSort.length;i++)
     { //krawędź do dodania
        let [eA,eB]=[edgesSort[i].a,edgesSort[i].b];
        //flaga czy krawędź jest ładna
        let eOk=1;
        {//test kolizji z innymi krawędziami
          for(let k=0;k<this.edges.length;k++)
          { let [A,B]=[this.edges[k].a,this.edges[k].b];
            if(this.#Collision_4id(A,B,eA,eB))eOk=0;
          }
        }
        {//test odległości od wierzchołków
          if(eOk)
            for(let k=0;k<this.nodes.length;k++)
              if((k!=eA)&&(k!=eB))
                if(this.#Distance_3id(eA,eB,k)<nodeDist)eOk=0;
        }
        {//test ostrego kąta z innymi krawędziami
          if(eOk)for(let k=0;k<this.edges.length;k++)
          { let[A,B]=[this.edges[k].a,this.edges[k].b];
            if(A==eA) if(this.#AngleCos_3id(B,A,eB)>cos)eOk=0;
            if(A==eB) if(this.#AngleCos_3id(B,A,eA)>cos)eOk=0;
            if(B==eA) if(this.#AngleCos_3id(A,B,eB)>cos)eOk=0;
            if(B==eB) if(this.#AngleCos_3id(A,B,eA)>cos)eOk=0;
          }
        }
        //dodajemy ładną krawędź
        if(eOk==1)
        {
          if(this.nodes[eA].y<this.nodes[eB].y) this.edges.push( {a:eA,b:eB} );
          if(this.nodes[eA].y>this.nodes[eB].y) this.edges.push( {a:eB,b:eA} );
          //this.edges.push({a:eA,b:eB});
        }
      }
    }
  }

  #IsSpace([x,y],dist)
  { //sprawdza czy współrzędne XY są dalej od zbioru NODES niż DIST//
    for(let i=0;i<this.nodes.length;i++)
    {
      let dx = (x-this.nodes[i].x);
      let dy = (y-this.nodes[i].y);
      if(dx*dx+dy*dy<dist*dist) return 0;
    }
    return 1;
  }

  #Distance_2id(a,b)
  { //odległość dwóch wierzchołków//
    let dx= this.nodes[a].x-this.nodes[b].x;
    let dy= this.nodes[a].y-this.nodes[b].y;
    return Math.sqrt( dx*dx+dy*dy );
  }

  #CrossProduct_3id(a,b,c)
  { //długość iloczynu wektorowego dla wektorów pomiędzy wierzhołkami//
    let ca0 = this.nodes[c].x-this.nodes[a].x;
    let ca1 = this.nodes[c].y-this.nodes[a].y;
    let ba0 = this.nodes[b].x-this.nodes[a].x;
    let ba1 = this.nodes[b].y-this.nodes[a].y;
    return ca0*ba1-ba0*ca1;
  }

  #Collision_4id(a,b,c,d)
  { //[0,1] przecięcie odcinków pomiędzy (a,b) z (c,d)//
    let v1=this.#CrossProduct_3id(c,d,a);
    let v2=this.#CrossProduct_3id(c,d,b);
    let v3=this.#CrossProduct_3id(a,b,c);
    let v4=this.#CrossProduct_3id(a,b,d);
    if((v1*v2<0)&&(v3*v4<0))return 1;
    return 0;
  }

  #AngleCos_3id(a,b,c)
  { //zwraca cosinus kąta pomiędzy (a,b,c)//
    let u= {x:(this.nodes[a].x-this.nodes[b].x),
            y:(this.nodes[a].y-this.nodes[b].y)};
    let v= {x:(this.nodes[c].x-this.nodes[b].x),
            y:(this.nodes[c].y-this.nodes[b].y)};
    let uv_skalar = u.x*v.x+u.y*v.y;
    let u_length  = Math.sqrt( u.x*u.x+u.y*u.y);
    let v_length  = Math.sqrt( v.x*v.x+v.y*v.y);
    let cosKat=uv_skalar/u_length/v_length;
    return cosKat;
  }

  #Distance_3id(a,b,c)
  { //zwraca odległość punktu C od odcinka AB//
    //jeżeli kąt ABC jest rozwarty zwraca odległość |BC|
    if(this.#AngleCos_3id(a,b,c)<=0)return this.#Distance_2id(b,c);
    // jeżeli kąt BAC jest rozwarty zwraca odległość |AC|
    if(this.#AngleCos_3id(b,a,c)<=0)return this.#Distance_2id(a,c);
    // zwraca wysokość trójkąta ABC
    var h=this.#CrossProduct_3id(a,b,c)/this.#Distance_2id(a,b);
    if(h<0)h=-h;
    return h;
  }

}

class Graph extends GraphXY
{ //klasa GRAFU z node:{x,y,pmin,pmod,pmax} //

  SetDataPDF()
  { //dane z prezentacji PDF//
    this.nodes.push( {x: 1,y:3,pmin:1,pmod:2,pmax:3 } ) //0:a
    this.nodes.push( {x: 1,y:6,pmin:2,pmod:3,pmax:4 } ) //1:b
    this.nodes.push( {x: 5,y:0,pmin:1,pmod:2,pmax:3 } ) //2:c
    this.nodes.push( {x: 5,y:3,pmin:1,pmod:2,pmax:3 } ) //3:d
    this.nodes.push( {x: 5,y:6,pmin:3,pmod:4,pmax:5 } ) //4:e
    this.nodes.push( {x: 9,y:6,pmin:2,pmod:4,pmax:6 } ) //5:f
    this.nodes.push( {x: 9,y:0,pmin:1,pmod:3,pmax:5 } ) //6:g
    this.nodes.push( {x: 9,y:3,pmin:3,pmod:5,pmax:7 } ) //7:h
    this.nodes.push( {x:13,y:6,pmin:5,pmod:7,pmax:9 } ) //8:i
    this.edges.push( {a:0,b:2} )
    this.edges.push( {a:0,b:3} )
    this.edges.push( {a:1,b:4} )
    this.edges.push( {a:2,b:6} )
    this.edges.push( {a:2,b:7} )
    this.edges.push( {a:3,b:5} )
    this.edges.push( {a:4,b:5} )
    this.edges.push( {a:7,b:8} )
    this.edges.push( {a:5,b:8} )
  }

  SetRand(nodeN)
  { //losuje graf//
    //losowanie xy,edges: funkcje dziedziczone po GraphXY
    this.SetNodesRand(nodeN,16-2,8-2,3.0);
    this.SetEdges(2,20);
    //losowanie tMin,tMod,tMax
    let pMax=9;
    for(let i=0; i<this.nodes.length;i++)
    {
      let pmin= 1+Math.floor(pMax*Math.random()) ;
      let pmod= 1+Math.floor(pMax*Math.random()) ;
      let pmax= 1+Math.floor(pMax*Math.random()) ;
      [pmin,pmod] = [ Math.min(pmin,pmod),Math.max(pmin,pmod)];
      [pmod,pmax] = [ Math.min(pmax,pmod),Math.max(pmax,pmod)];
      [pmin,pmod] = [ Math.min(pmin,pmod),Math.max(pmin,pmod)];
      this.nodes[i].pmin=pmin;
      this.nodes[i].pmod=pmod;
      this.nodes[i].pmax=pmax;
    }
  }

  QCPM(p)
  { //metda scieżki krytycznej//
    { //tworzy R
      var r=[]; for(let i=0;i<this.nodes.length;i++)r.push(p[i])
      for(let n=0; n<this.edges.length; n++)for(let i=0; i<this.edges.length; i++)
      { let [a,b] = [this.edges[i].a, this.edges[i].b];
        r[b] = Math.max( r[b],r[a]+p[b] );
      }
    }
    { //tworzy cmax, operCmax, operCmaxN
      var cmax=0,operCmax=0,operCmaxN=0;
      for(let o=0;o<this.nodes.length;o++)
        cmax=Math.max(cmax,r[o]);
      for(let o=0;o<this.nodes.length;o++)if(r[o]==cmax)
       {operCmax=o;operCmaxN++;}
    }
    { //tworzy path, multiPath
      var multiPath=(operCmaxN>1);
      var path=[];
      let oper=operCmax;
      while(oper>-1)
      {
        path.unshift(oper);
        let prev=-1;
        let prevN=0;
        for(let i=0;i<this.edges.length;i++)if(this.edges[i].b==oper)
        {
          let a= this.edges[i].a
          if(prev==-1)prev=a;
          if(r[a]>r[prev]){prev=a;prevN=0;}
          if(r[a]==r[prev])prevN++;
        }
        multiPath+=(prevN>1);
        oper=prev;
      }
    }
    return { cmax:cmax, path:path, ef:r };
  }

  PERT()
  { //metoda PERT
    let pavg=[];
    let pvar=[];
    for(let i=0;i<this.nodes.length;i++)
    { let N=this.nodes[i];
      pavg.push( (N.pmin + 4*N.pmod + N.pmax)/6   );
      pvar.push( (N.pmax-N.pmin)*(N.pmax-N.pmin)/6/6 );
    }
    let path=[]
    let cavg=0;
    let csig=0;

    let cpm = this.QCPM(pavg);
    let cvar = 0;
    for(let i=0;i<cpm.path.length;i++)
      cvar += pvar[cpm.path[i]];
    csig = Math.sqrt(cvar);
    gauss.avg = cpm.cmax;
    gauss.sig = csig;
    return {pavg:pavg,pvar:pvar,path:cpm.path,cavg:cpm.cmax,csig:csig,ef:cpm.ef};
  }

}

class TXT
{ // wyswietlanie przy pomocy Text //

  static DrawBoxGraph(box,graf)
  { //wypisuje na box tabelę danych
    let txt='<div style="text-align:center; padding-top:20px;">';
    txt+= this.#GetTxtData(graf);
    txt+='</div>';
    document.getElementById(box).innerHTML=txt;
  }

  static DrawBoxPert(box,graf,pert)
  { //wypisuje na box tabelę PERT
    let txt='<div style="text-align:center; padding-top:20px">';
    txt+= this.#GetTxtPert(graf,pert);
    txt += '</div>';
    document.getElementById(box).innerHTML=txt;
  }

  static DrawBoxQuest(box)
  { //wypisuje na box tabelę PERT
    let txt='<div style="text-align:center; padding-top:60px;">';
    txt +='czas projektu:\n\n';
    txt +='<input id="inpTime"  type="text" '
        +'style="width:20%;background-color:#322;color:#766" />\n\n'
    txt +='szansa powodzenia:\n\n';
    txt +='<input id="inpProb"  type="text" '
        +'style="width:20%;background-color:#322;color:#766" />\n\n'
    txt+='</div>';
    document.getElementById(box).innerHTML=txt;
  }

  static #GetTxtData(graf)
  { //zwraca tabelę danych
    let txt='';
    txt += ' nr | p.min p.mod p.max | następnicy   \n';
    txt += '---------------------------------------\n';
    for(let i=0; i<graf.nodes.length; i++)
    { //lista następników węzła i
      let node=graf.nodes[i];
      let next='',nextN=0;
      for(let ii=0;ii<graf.edges.length; ii++)
        if(graf.edges[ii].a==i)
          next+=String.fromCharCode(65+graf.edges[ii].b)+' ';
      if(next=='')next='- ';
      txt += '  '+String.fromCharCode(65+i)+' |';
      txt += this.#TxtR(node.pmin,6);
      txt += this.#TxtR(node.pmod,6);
      txt += this.#TxtR(node.pmax,6)+' | ';
      txt += this.#TxtL(next,13);
      txt += '\n'
    }
    return txt;
  }

  static #GetTxtPert(graf,pert)
  { //zwraca tabelę PERT
    let nodes = graf.nodes;
    let pathTxt='';
    for(let i=0;i<pert.path.length;i++)
    {
      if(i) pathTxt += ','
      pathTxt += String.fromCharCode(65+pert.path[i])
    }
    let txt='';
    txt += 'ścieżka=( '+pathTxt+' )'
    txt += ', μ='+pert.cavg.toFixed(2)+', σ='+pert.csig.toFixed(2)+'\n\n';
    txt += ' nr | p.avg p.var |    ES    EF \n';
    txt += '--------------------------------\n';
    for(let i=0,ii=0; i<graf.nodes.length; i++)
    {
      txt += '  '+String.fromCharCode(65+i)+' | ';
      txt += this.#TxtR(pert.pavg[i].toFixed(2),5)+' ';
      txt += this.#TxtR(pert.pvar[i].toFixed(2),5)+' |';
      txt += this.#TxtR((pert.ef[i]-pert.pavg[i]).toFixed(2),6)+' ';
      txt += this.#TxtR(pert.ef[i].toFixed(2),5)+' ';
      txt += '\n';
    }
    //txt = txt.replaceAll('\n','.\n')
    return txt;
  }

  static #TxtR(str,n)
  { //wyrównuje text do prawej//
    let out = String(str);
    let l = out.length;
    while(l<n) { l++; out = ' '+out;}
    return out
  }

  static #TxtL(str,n)
  { //wyrównuje text do lewej//
    let out = String(str);
    let l = out.length;
    while(l<n) { l++; out+=' ';}
    return out
  }

}

class SVG
{ // wyswietlanie przy pomocy Svg //

  static DrawBoxGraph(box,graf)
  { //rysuje graf
    let svg = '<svg width="440" height="240">';
    svg+=this.#GetDatHead();
    svg+=this.#GetDatGrid();
    svg+=this.#GetDatGraf(graf);
    svg+='</svg>';
    document.getElementById(box).innerHTML=svg;
  }

  static DrawBoxPert(box,graf,pert)
  { //rysuje pert (graf z p.avg, p.var i PATH)
    let svg = '<svg width="440" height="240">';
    svg+=this.#GetDatHead();
    svg+=this.#GetDatGrid();
    svg+=this.#GetDatPert(graf,pert);
    svg+='</svg>';
    document.getElementById(box).innerHTML=svg;
  }

  static #GetXY(graph,i)
  { //zwraca przeskalowane wspołrzędne XY używane do rysowania//
    return {x:40+20*graph.nodes[i].x, y:40+20*graph.nodes[i].y};
  }

  static #GetDatGrid()
  { //dane svg:grid
    let svg="";
    svg+='<g style="stroke: #271717; stroke-width:1; fill: none;">';
    svg+='<path d="M 20 30';
    for(var i=0;i<10;i++)svg+='m -10 0, l 420 0, m -410 20';
    svg+='M 30 20';
    for(var i=0;i<20;i++)svg+='m 0 -10, l 0 220, m 20 -210';
    svg+='"/></g>';
    svg+='<g style="stroke: #2f1f1f; stroke-width:1; fill: none;">';
    svg+='<path d="M 20 20';
    for(var i=0;i<=10;i++)svg+='m -10 0, l 420 0, m -410 20';
    svg+='M 20 20';
    for(var i=0;i<=20;i++)svg+='m 0 -10, l 0 220, m 20 -210';
    svg+='"/></g>';
    return svg;
  }

  static #CutLine(a,b,d)
  { //przycina odcinek A-B od strony konca B o długość d
    var [dx,dy]=[a.x-b.x,a.y-b.y];
    let dist = Math.sqrt( dx*dx+dy*dy );
    let proc = d/dist;
    return {x:(a.x*proc+b.x*(1-proc)), y:(a.y*proc+b.y*(1-proc))};
  }

  static #GetDatHead()
  { //dane svg nagłówek
  let svg=' <marker'
      + '    id="arrow" '
      + '    stroke-width="0.1" stroke="#322" fill="#322"'
      + '    viewBox="-4 -3 6 6"'
      + '    refX="0" refY="0"'
      + '    markerWidth="6" markerHeight="6"'
      + '    orient="auto-start-reverse">'
      + '    <path d="M -2 0 L -4 -2 L 2 0 L -4 2 z" />'
      + '  </marker>'
      + ' <marker'
      + '    id="arrowR" '
      + '    stroke-width="0.1" stroke="#766" fill="#766"'
      + '    viewBox="-4 -3 6 6"'
      + '    refX="0" refY="0"'
      + '    markerWidth="6" markerHeight="6"'
      + '    orient="auto-start-reverse">'
      + '    <path d="M -2 0 L -4 -2 L 2 0 L -4 2 z" />'
      + '  </marker>'
      + '  <style>'
      + '    <![CDATA[#edge {stroke:#322; stroke-width:2; marker-end:url(#arrow) ; } ]]>'
      + '    <![CDATA[#edgeR{stroke:#766; stroke-width:2; marker-end:url(#arrowR); } ]]>'
      + '    <![CDATA[#node {stroke:#322; stroke-width:2; fill:#211; } ]]>'
      + '    <![CDATA[#nodeR{stroke:#766; stroke-width:2; fill:#211; } ]]>'
      + '    <![CDATA[#text {text-anchor:middle; dominant-baseline:middle;font-size:9px;fill:#322;} ]]>'
      + '    <![CDATA[#textR{text-anchor:middle; dominant-baseline:middle;font-size:9px;fill:#766;} ]]>'
      + '    <![CDATA[#textB{text-anchor:middle; dominant-baseline:middle;font-size:16px;fill:#766;} ]]>'
      + '  </style> '
    return svg
  }

  static #GetDatGraf(graf)
  { //dane svg graf
    let svg='';
    //krawędzie
    for(var i=0; i<graf.edges.length; i++ )
    { let [aId,bId] = [graf.edges[i].a, graf.edges[i].b];
      let [aXY,bXY] = [this.#GetXY(graf,aId),this.#GetXY(graf,bId)];
      let eB = this.#CutLine( aXY,bXY,27+4 );
      let eA = this.#CutLine( bXY,aXY,23+4 );
      svg+='<line id="edgeR" x1="'+eA.x+'" y1="'+eA.y+'" x2="'+eB.x+'" y2="'+eB.y+'"/>';
    }
    //wierzchołki
    for(var i=0; i<graf.nodes.length; i++ )
    { let xy = this.#GetXY(graf,i);
      let y1 = xy.y-4;
      let y2 = xy.y+8;
      let text1 = String.fromCharCode(65+i);
      let text2 = graf.nodes[i].pmin+':'+graf.nodes[i].pmod+':'+graf.nodes[i].pmax;
      svg+='<circle id="nodeR" cx="'+xy.x+'" cy="'+xy.y+'" r="22"/>';
      svg+='<text id="textB" x="'+xy.x+'" y="'+y1+'" >'+ text1 +'</text>';
      svg+='<text id="textR" x="'+xy.x+'" y="'+y2+'" >'+ text2 +'</text>';
    }
    return svg;
  }

  static #GetDatPert(graf,pert)
  { //dane svg cpm
    let svg='';
    //krawędzie
    for(var i=0; i<graf.edges.length; i++ )
    { let [aId,bId] = [graf.edges[i].a, graf.edges[i].b];
      let [aXY,bXY] = [this.#GetXY(graf,aId),this.#GetXY(graf,bId)];
      let eB = this.#CutLine( aXY,bXY,27+4 );
      let eA = this.#CutLine( bXY,aXY,23+4 );
      let style="";
      for(let k=1;k<pert.path.length;k++)
        if((pert.path[k-1]==aId)&&(pert.path[k]==bId))style="R";
      svg+='<line id="edge'+style+'" x1="'+eA.x+'" y1="'+eA.y+'" x2="'+eB.x+'" y2="'+eB.y+'"/>';
    }
    //wierzchołki
    for(var i=0; i<graf.nodes.length; i++ )
    { let xy = this.#GetXY(graf,i);
      let y0 = xy.y+ 0;
      let y1 = xy.y- 10;
      let y2 = xy.y+ 10;
      let text = String.fromCharCode(65+i)+':'+pert.pavg[i].toFixed(1);
      let text1 =pert.ef[i].toFixed(1);
      let text2 =pert.pvar[i].toFixed(2);
      let style=""
      if( pert.path.includes(i)) style="R";
      svg+='<circle id="node'+style+'" cx="'+xy.x+'" cy="'+xy.y+'" r="22"/>';
      style='R';
      svg+=  '<text id="text'+style+'" x="'+xy.x+'" y="'+y0+'" >'+ text +'</text>';
      svg+=  '<text id="text'+style+'" x="'+xy.x+'" y="'+y1+'" >'+ text1 +'</text>';
      svg+=  '<text id="text'+style+'" x="'+xy.x+'" y="'+y2+'" >'+ text2 +'</text>';
     }
    return svg;
  }
}

class CAN
{ // wyświetlanie przy pomocy Canvas //
  static DrawBoxGraph(box,graf)
  { //rysuje na Box'ie graf
    document.getElementById(box).innerHTML= '<canvas id="canGraph"</canvas>';
    let canvas = document.getElementById("canGraph");
    let ctx = canvas.getContext("2d");
    this.#SetCanvasCtxSize(canvas,ctx,480,240);
    this.#DrawCtxGrid(ctx);
    this.#DrawCtxGraph(ctx,graf);
  }

  static DrawBoxPert(box,graf,pert)
  { //rysuje na Box'ie pert
    document.getElementById(box).innerHTML= '<canvas id="canPert"</canvas>';
    let canvas = document.getElementById("canPert");
    let ctx = canvas.getContext("2d");
    this.#SetCanvasCtxSize(canvas,ctx,480,240);
    this.#DrawCtxGrid(ctx);
    this.#DrawCtxPert(ctx,graf,pert);
  }

  static DrawBoxFunc(box,x)
  { //rysuje na Box'ie pert
    document.getElementById(box).innerHTML= '<canvas id="canFunc"</canvas>';
    let canvas = document.getElementById("canFunc");
    let ctx = canvas.getContext("2d");
    this.#SetCanvasCtxSize(canvas,ctx,480,240);
    //this.#DrawCtxGrid(ctx);
    this.#DrawCtxGridStart(ctx,gauss.avg-4);
    this.#DrawCtxDistribution(ctx,x);
  }

  static #SetCanvasCtxSize(canvas,ctx,width,height)
  { //ustawia aby 1px ctx był jednym pixelem ekranu
    var devicePixelRatio = window.devicePixelRatio || 1;
    canvas.width  =  width * devicePixelRatio;
    canvas.height =  height * devicePixelRatio;
    canvas.style.width  = width + 'px';
    canvas.style.height = height + 'px';
    ctx.scale(devicePixelRatio, devicePixelRatio)
  }

  static #DrawCtxGrid(ctx)
  { //dane svg:grid
    ctx.strokeStyle = '#271717'
    ctx.lineWidth = '1'
    ctx.beginPath();
    for(let i=0;i<=40;i++) {ctx.moveTo(10,20+i*5); ctx.lineTo(430,20+i*5);}
    for(let i=0;i<=80;i++) {ctx.moveTo(20+i*5,10); ctx.lineTo(20+i*5,230);}
    ctx.stroke();

    ctx.beginPath();
    ctx.strokeStyle = '#2c1c1c'
    ctx.lineWidth = '1'
    for(let i=0;i<=8;i++)  {ctx.moveTo(10,20+i*25); ctx.lineTo(430,20+i*25);}
    for(let i=0;i<=16;i++) {ctx.moveTo(20+i*25,10); ctx.lineTo(20+i*25,230);}
    ctx.stroke();

    ctx.beginPath();
    ctx.strokeStyle = '#2f1f1f'
    ctx.lineWidth = '1'
    for(let i=0;i<=4;i++)  {ctx.moveTo(10,20+i*50); ctx.lineTo(430,20+i*50);}
    for(let i=0;i<=8;i++) {ctx.moveTo(20+i*50,10); ctx.lineTo(20+i*50,230);}
    ctx.stroke();
  }

  static #DrawCtxGridStart(ctx,start)
  { //dane svg:grid
    ctx.strokeStyle = '#271717'
    ctx.lineWidth = '1'
    ctx.beginPath();
    for(let i=0;i<=40;i++) {ctx.moveTo(15,20+i*5); ctx.lineTo(425,20+i*5);}
    //for(let i=0;i<=80;i++) {ctx.moveTo(20+i*5,10); ctx.lineTo(20+i*5,230);}
    var sh=(-start*10+Math.ceil(start*10))*5;
    if(sh<0)sh+=5;
    for(let i=sh;i<=400;i+=5)
      {ctx.moveTo(20+i,15); ctx.lineTo(20+i,225);}
    ctx.stroke();

    ctx.beginPath();
    ctx.strokeStyle = '#2c1c1c'
    ctx.lineWidth = '1'
    for(let i=0;i<=8;i++)  {ctx.moveTo(15,20+i*25); ctx.lineTo(425,20+i*25);}
    //for(let i=0;i<=16;i++) {ctx.moveTo(20+i*25,10); ctx.lineTo(20+i*25,230);}
    var sh=(-start*2+Math.ceil(start*2))*25;
    if(sh<0)sh+=25;
    for(let i=sh;i<=400;i+=25)
      {ctx.moveTo(20+i,15); ctx.lineTo(20+i,225);}
    ctx.stroke();


    ctx.beginPath();
    ctx.strokeStyle = '#2f1f1f'
    ctx.lineWidth = '1'
    for(let i=0;i<=4;i++)  {ctx.moveTo(15,20+i*50); ctx.lineTo(425,20+i*50);}
    var sh=(-start+Math.ceil(start))*50;
    if(sh<0)sh+=50;
    for(let i=sh;i<=400;i+=50)
      {ctx.moveTo(20+i,15); ctx.lineTo(20+i,225);}

    ctx.stroke();
  }


  static #GetXY(graph,i)
  { //zwraca przeskalowane wspołrzędne XY używane do rysowania//
    return {x:45+25*graph.nodes[i].x, y:45+25*graph.nodes[i].y};
  }

  static #DrawArrow(ctx, a0, b0)
  {
    var [d0x,d0y]=[b0.x-a0.x,b0.y-a0.y];
    let dist0 = Math.sqrt( d0x*d0x+d0y*d0y );
    let distA0 = 28/dist0;
    let distB0 = 28/dist0;
    let a = {x: a0.x+distA0*d0x, y:a0.y+distA0*d0y } //początek strzałki
    let b = {x: b0.x-distB0*d0x, y:b0.y-distB0*d0y } //koniec strzałki

    const [dx,dy]=[b.x-a.x,b.y-a.y];
    let   dist  = Math.sqrt( dx*dx+dy*dy );
    let   dist1    =  7/dist;
    let   dist2    = 10/dist;
    let   dist3    =  3/dist;

    let c = { x:b.x-dist1*dx, y:b.y-dist1*dy } //tył strzałki
    let d = { x:b.x-dist2*dx, y:b.y-dist2*dy } //rzut wierzchołka strzałki
    let e = { x:d.x-dist3*dy, y:d.y+dist3*dx } //pierwszy wierzchołek strzałki
    let f = { x:d.x+dist3*dy, y:d.y-dist3*dx } //drugi wierzchołek strzałki

    ctx.lineWidth = '1'
    ctx.beginPath();
    ctx.moveTo(c.x, c.y);
    ctx.lineTo(e.x, e.y);
    ctx.lineTo(b.x, b.y);
    ctx.lineTo(f.x, f.y);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();

    ctx.lineWidth = '2'
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(c.x, c.y);
    ctx.stroke();
  }

  static #DrawCtxGraph(ctx,graf)
  {
    //krawędzie
    ctx.lineWidth = '1'
    ctx.strokeStyle = '#766'
    ctx.fillStyle = '#766'
    for(var i=0; i<graf.edges.length; i++ )
    { let [aId,bId] = [graf.edges[i].a, graf.edges[i].b];
      let [aXY,bXY] = [this.#GetXY(graf,aId),this.#GetXY(graf,bId)];
      this.#DrawArrow(ctx,aXY,bXY);
    }

    //wierzchołki
    ctx.lineWidth = '2'
    ctx.strokeStyle = '#766'
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';
    for(var i=0; i<graf.nodes.length; i++ )
    { let xy = this.#GetXY(graf,i);
      let y1 = xy.y-4;
      let y2 = xy.y+8;
      let text1 = String.fromCharCode(65+i);
      let text2 = graf.nodes[i].pmin+':'+graf.nodes[i].pmod+':'+graf.nodes[i].pmax;

      ctx.fillStyle = '#211'//'rgba(40, 30, 30, 0.5)';
      ctx.beginPath(); ctx.arc(xy.x,xy.y,22,0,6.3); ctx.fill();
      ctx.fillStyle = '#766';  ctx.font = "16px Courier";
      ctx.fillText(text1,xy.x,y1);
      ctx.font = "9px Courier";
      ctx.fillText(text2,xy.x,y2);
      ctx.stroke();
    }

  }

  static #DrawCtxPert(ctx,graf,pert)
  {
    //krawędzie
    for(var i=0; i<graf.edges.length; i++ )
    { let [aId,bId] = [graf.edges[i].a, graf.edges[i].b];
      let [aXY,bXY] = [this.#GetXY(graf,aId),this.#GetXY(graf,bId)];

      ctx.lineWidth = '1'
      ctx.strokeStyle = '#433'
      ctx.fillStyle = '#433'
      for(let k=1;k<pert.path.length;k++)
        if((pert.path[k-1]==aId)&&(pert.path[k]==bId))
          {ctx.strokeStyle='#766'; ctx.fillStyle = '#766'}
      this.#DrawArrow(ctx,aXY,bXY);
    }

    //wierzchołki
    ctx.lineWidth = '2'
    ctx.strokeStyle = '#766'
    ctx.fillStyle = '#211'
    ctx.font = "12px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';
    for(var i=0; i<graf.nodes.length; i++ )
    { let xy = this.#GetXY(graf,i);
      let y0 = xy.y +0;
      let y1 = xy.y- 10;
      let y2 = xy.y+ 10;
      let text0 = String.fromCharCode(65+i)+':'+pert.pavg[i].toFixed(1);
      let text1 =pert.ef[i].toFixed(1);
      let text2 =pert.pvar[i].toFixed(2);
      let light = pert.path.includes(i);

      ctx.fillStyle = '#211'; ctx.strokeStyle = '#433'
      if(light) ctx.strokeStyle = '#766';
      ctx.beginPath(); ctx.arc(xy.x,xy.y,22,0,6.3); ctx.fill();

      ctx.fillStyle = '#433'; ctx.textAlign = "center"; ctx.font = "9px Courier";
      if(light)ctx.fillStyle = '#766';
      ctx.fillText(text0,xy.x,y0);
      ctx.fillText(text1,xy.x,y1);
      ctx.fillText(text2,xy.x,y2);
      ctx.stroke();
    }

  }

  static #DrawCtxDistribution(ctx,x)
  {
    // x to zaznacza wartość na wykresie (długość projektu)
    const imgWidth =  400;                     //liczba pixeli wykresu
    const imgXmin  =  gauss.avg-4;             //najmniejsza wartość x
    const imgXscl  =  50;                      //skala ile pixeli na 1 T
    const imgYscl  = 120/gauss.sig;            //skala sigma
    const imgT     = -Math.floor(-imgXmin);    //najmniejszy opis wartość
    const imgPosT  = ((imgT)-imgXmin)*imgXscl; //najmniejszy opis pozycja
    let   imgPosX  = ((  x )-imgXmin)*imgXscl; //pozycja X
          imgPosX  = Math.min(400,imgPosX);
    const imgY =195;


    { //oś
      ctx.beginPath();
      ctx.lineWidth = '1'
      ctx.strokeStyle = '#655'
      ctx.moveTo(10,imgY)
      ctx.lineTo(430,imgY)
      ctx.stroke();

      //opis osi z kreską
      ctx.font = "12px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#655'
      ctx.lineWidth = '1'
      ctx.strokeStyle = '#655'
      for(let T=imgT,i=imgPosT; i<=400; i+=imgXscl,T+=1)
      {
        ctx.beginPath();
        ctx.fillText(T,20+i,imgY+15);
        ctx.moveTo  (20+i,imgY);
        ctx.lineTo  (20+i,imgY+5);
        ctx.stroke();
      }
    }

    { //opis wykresu
      ctx.beginPath();
      ctx.font = "12px Arial";
      ctx.textAlign = "left";
      ctx.textBaseline = 'middle';
      ctx.fillStyle = "#766";
      let txt='N( μ='+gauss.avg.toFixed(2)+', σ='+gauss.sig.toFixed(2)+' )';
      ctx.fillText(txt,40,30);
    }


    { // górna linia gaussa
      ctx.beginPath();
      ctx.lineWidth = '2'
      ctx.strokeStyle = '#766'
      for(var i=0; i<imgWidth; i++ )
      {
        let x= imgXmin + i/imgXscl;
        let y= Math.exp(-((x-gauss.avg)*(x-gauss.avg))/gauss.sig/gauss.sig)
        if(i==0) ctx.moveTo(20+i,imgY-imgYscl*y);
        else     ctx.lineTo(20+i,imgY-imgYscl*y);
      }
      ctx.stroke()
    }


    { //wypełnienie gaussa
      ctx.beginPath();
      ctx.fillStyle = "rgba(40, 80, 40, 0.5)";
      ctx.moveTo(20,imgY)
      for(var i=0; i<=imgPosX; i++ )
      {
        let x= imgXmin + i/imgXscl;
        var y= Math.exp(-((x-gauss.avg)*(x-gauss.avg))/gauss.sig/gauss.sig)
        ctx.lineTo(20+i,imgY-imgYscl*y);
      }
      ctx.lineTo(20+i,imgY);
      ctx.fill();
    }

    {//kreska za sielonym polem
      ctx.beginPath();
      ctx.lineWidth = '1'
      ctx.strokeStyle = "#766"
      if(imgPosX<imgWidth&&imgPosX>0)
      {
        ctx.lineTo(20+imgPosX,imgY-imgYscl*y);
        ctx.lineTo(20+imgPosX,imgY);
        ctx.stroke();
      }
    }

  }

}

class Click
{ // zbiór funkcji: wywoływanych po kliknięciu //

  static DrawPDF()
  {
    let graf=new Graph();
    graf.SetDataPDF();
    let pert = graf.PERT();
    TXT.DrawBoxGraph("boxDat1", graf );
    CAN.DrawBoxGraph("boxDat2", graf );
    TXT.DrawBoxPert("boxDat3", graf, pert );
    CAN.DrawBoxPert("boxDat4", graf, pert );
    document.getElementById('inpProb').value='0.50';
    Click.EnterProb();
  }

  static ClickRand()
  {
    let graf=new Graph();
    graf.SetRand(10);
    let pert = graf.PERT();
    TXT.DrawBoxGraph("boxDat1", graf );
    CAN.DrawBoxGraph("boxDat2", graf );
    TXT.DrawBoxPert("boxDat3", graf, pert );
    CAN.DrawBoxPert("boxDat4", graf, pert );
    document.getElementById('inpProb').value='0.5';
    Click.EnterProb();
  }

  static EnterTime()
  {
    let time = Number(document.getElementById('inpTime').value);
    let prob = gauss.Cdf( gauss.Scale(time) );
    document.getElementById('inpProb').value=(prob).toFixed(4);
    CAN.DrawBoxFunc("boxDat6", time );
  }

  static EnterProb()
  {
    let prob = Number(document.getElementById('inpProb').value);
    let time = gauss.ScaleInv(gauss.CdfInv(prob));
    document.getElementById('inpTime').value=time.toFixed(2);
    CAN.DrawBoxFunc("boxDat6", time );
  }

}


function Init()
{ // funkcja uruchamiana przy starcie strony //
  document.onselectstart = function(){return false;};
  document.getElementById('btnRand').addEventListener('click',Click.ClickRand);
  TXT.DrawBoxQuest('boxDat5');
  Click.DrawPDF();

  document.getElementById('inpTime').addEventListener('keypress',
    function(e){if(e.key=='Enter'){Click.EnterTime();}});

  document.getElementById('inpProb').addEventListener('keypress',
    function(e){if(e.key=='Enter'){Click.EnterProb();}});

}

Init();
