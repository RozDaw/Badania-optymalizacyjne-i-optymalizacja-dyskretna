///////////////////////////////////////////////////////////
////                                                  /////
////  Interakcja strony CPM                           /////
////                                                  /////
///////////////////////////////////////////////////////////


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
{ // klasa GRAFU z node:{x,y,p} //

  SetDataPDF()
  {
    this.nodes.push( {x: 2,y: 1,p:2 } ) //0:a
    this.nodes.push( {x: 2,y: 7,p:5 } ) //1:b
    this.nodes.push( {x: 9,y: 1,p:1 } ) //2:c
    this.nodes.push( {x: 9,y: 7,p:6 } ) //3:d
    this.nodes.push( {x:16,y: 1,p:4 } ) //4:e
    this.nodes.push( {x:16,y: 7,p:2 } ) //5:f
    this.edges.push( {a:0,b:2} ) //a-c
    this.edges.push( {a:1,b:2} ) //b-c
    this.edges.push( {a:1,b:3} ) //b-d
    this.edges.push( {a:2,b:4} ) //c-e
    this.edges.push( {a:3,b:4} ) //d-e
    this.edges.push( {a:3,b:5} ) //d-f
  }

  SetRand(nodeN)
  { //losuje graf
    this.SetNodesRand(nodeN,18,8,3.8);
    this.SetEdges(2,20);
    //losowanie p
    let pMax=9;
    for(let i=0; i<this.nodes.length;i++)
    {
      let p= 1+Math.floor(pMax*Math.random()) ;
      this.nodes[i].p=p;
    }
  }

  CPM()
  { //metda scieżki krytycznej
    { //tworzy R Q
      var r=[],q=[]; for(let i=0;i<this.nodes.length;i++)
        {r.push(this.nodes[i].p);q.push(this.nodes[i].p)};
      for(let n=0; n<this.edges.length; n++)for(let i=0; i<this.edges.length; i++)
      { let [a,b] = [this.edges[i].a, this.edges[i].b];
        r[b] = Math.max( r[b],r[a]+this.nodes[b].p );
        q[a] = Math.max( q[a],q[b]+this.nodes[a].p );
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
    { //tworzy es,ls,lf (rf=r)
      var es=[],ls=[],lf=[];
      for(let i=0; i<this.nodes.length; i++)
      {
        es.push( r[i]-this.nodes[i].p );
        ls.push( cmax-q[i] );
        lf.push( cmax-q[i]+this.nodes[i].p );
      }
    }
    return { cmax:cmax, path:path, es:es, ef:r, ls:ls, lf:lf };
  }

}

class DrawTxt
{ // zbiór funkcji: wypisywanie TXT //

  static DrawTxtDatA(box,graf)
  { //wypisuje na box tabelę CPM
    let txt='<div style="padding:40px">';
    txt+= this.TxtDatA(graf);
    txt += '</div>';
    document.getElementById(box).innerHTML=txt;
  }

  static DrawTxtDatB(box,graf)
  { //wypisuje na box tabelę CPM
    let txt='<div style="text-align:center; padding-top:20px">';
    txt+= this.TxtDatB(graf);
    txt += '</div>';
    document.getElementById(box).innerHTML=txt;
  }

  static DrawTxtCpm(box,graf,cpm)
  { //wypisuje na box tabelę CPM
    let txt='<div style="text-align:center; padding-top:20px">';
    txt+= this.TxtCpm(graf,cpm);
    txt += '</div>';
    document.getElementById(box).innerHTML=txt;
  }

  static TxtR(str,n)
  { //wyrównuje text do prawej//
    let out = String(str);
    let l = out.length;
    while(l<n) { l++; out = ' '+out;}
    return out
  }

  static TxtL(str,n)
  { //wyrównuje text do lewej//
    let out = String(str);
    let l = out.length;
    while(l<n) { l++; out+=' ';}
    return out
  }

  static TxtDatA(graf)
  { //wypisuje na box listę krawędzi (Edge List)
    let txt='';//'<div style="padding:40px;";>';
    txt+='zbiór wierzchołków:\n'
    for(let i=0;i<graf.nodes.length;i++)
      txt+= String.fromCharCode(65+i)+':'+ graf.nodes[i].p+'  ';
    txt+='\n\n';
    txt+='zbiór krawędzi:\n'
    for(let i=0;i<graf.edges.length;i++)
    {
      if(i&&(i%10==0))txt+='\n';
      txt+=String.fromCharCode(65+graf.edges[i].a)+'-'+String.fromCharCode(65+graf.edges[i].b)+'  ';
    }
    return txt;
  }

  static TxtDatB(graf)
  { //wypisuje na box listę następników grafu (Adjacency List)
    let txt='';
    txt += ' nr | czas | następnicy   \n';
    txt += '--------------------------\n';
    for(let i=0; i<graf.nodes.length; i++)
    { //lista następników węzła i
      let next='',nextN=0;
      for(let ii=0;ii<graf.edges.length; ii++)
        if(graf.edges[ii].a==i)
          next+=String.fromCharCode(65+graf.edges[ii].b)+' ';
      if(next=='')next='- ';
      txt += '  '+String.fromCharCode(65+i)+' |';
      txt += this.TxtR(graf.nodes[i].p,5)+' | ';
      txt += this.TxtL(next,13);
      txt += '\n'
    }
    return txt;
  }

  static TxtCpm(graf,cpm)
  {
    let nodes = graf.nodes;
    let pathTxt='';
    for(let i=0;i<cpm.path.length;i++)
    {
      if(i) pathTxt += ','
      pathTxt += String.fromCharCode(65+cpm.path[i])
    }

    let txt='';
    txt += 'ścieżka=( '+pathTxt+' ), Cmax='+cpm.cmax+'\n\n';
    txt += ' nr | ES EF | LS LF | luz \n';
    txt += '--------------------------\n';
    for(let i=0,ii=0; i<graf.nodes.length; i++)
    {
      txt += '  '+String.fromCharCode(65+i)+' | ';
      txt += this.TxtR(cpm.es[i],3)+this.TxtR(cpm.ef[i],3)+' |';
      txt += this.TxtR(cpm.ls[i],3)+this.TxtR(cpm.lf[i],3)+' |';
      txt += this.TxtR(cpm.lf[i]-cpm.ef[i],4)+' ';
      txt += '\n';
    }
    return txt;
  }

}

class DrawSvg
{ // zbór funkcji: rysowanie SVG //
  static DrawSvgGraf(box,graf)
  { //rysuje graf
    let svg = '<svg width="440" height="240">';
    svg+=this.#GetDatHead();
    svg+=this.#GetDatGrid();
    svg+=this.#GetDatGraf(graf);
    svg+='</svg>';
    document.getElementById(box).innerHTML=svg;
  }

  static DrawSvgCpm(box,graf,cpm)
  { //rysuje Cpm (graf z ES,EF,LS,LF i PATH)
    let svg = '<svg width="440" height="240">';
    svg+=this.#GetDatHead();
    svg+=this.#GetDatGrid();
    svg+=this.#GetDatCpm(graf,cpm);
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
      let y1 = xy.y+1;
      let text = String.fromCharCode(65+i)+':'+graf.nodes[i].p;
      svg+='<circle id="nodeR" cx="'+xy.x+'" cy="'+xy.y+'" r="22"/>';
      svg+='<text id="textB" x="'+xy.x+'" y="'+y1+'" >'+ text +'</text>';
    }
    return svg;
  }

  static #GetDatCpm(graf,cpm)
  { //dane svg cpm
    let svg='';
    //krawędzie
    for(var i=0; i<graf.edges.length; i++ )
    { let [aId,bId] = [graf.edges[i].a, graf.edges[i].b];
      let [aXY,bXY] = [this.#GetXY(graf,aId),this.#GetXY(graf,bId)];
      let eB = this.#CutLine( aXY,bXY,27+4 );
      let eA = this.#CutLine( bXY,aXY,23+4 );
      let style="";
      for(let k=1;k<cpm.path.length;k++)
        if((cpm.path[k-1]==aId)&&(cpm.path[k]==bId))style="R";
      svg+='<line id="edge'+style+'" x1="'+eA.x+'" y1="'+eA.y+'" x2="'+eB.x+'" y2="'+eB.y+'"/>';
    }
    //wierzchołki
    for(var i=0; i<graf.nodes.length; i++ )
    { let xy = this.#GetXY(graf,i);
      let y0 = xy.y+ 1;
      let y1 = xy.y- 9;
      let y2 = xy.y+ 11;
      let text = String.fromCharCode(65+i)+':'+graf.nodes[i].p;
      let text1 =''+ (cpm.es[i])+'-'+(cpm.ef[i]);
      let text2 =''+ (cpm.ls[i])+'-'+(cpm.lf[i]);
      let style=""
      if( cpm.path.includes(i)) style="R";
      svg+='<circle id="node'+style+'" cx="'+xy.x+'" cy="'+xy.y+'" r="22"/>';
      style='R';
      svg+=  '<text id="text'+style+'" x="'+xy.x+'" y="'+y0+'" >'+ text +'</text>';
      svg+=  '<text id="text'+style+'" x="'+xy.x+'" y="'+y1+'" >'+ text1 +'</text>';
      svg+=  '<text id="text'+style+'" x="'+xy.x+'" y="'+y2+'" >'+ text2 +'</text>';
     }
    return svg;
  }

}

class Click
{ // zbiór funkcji: wywoływanych po kliknięciu //
  static DrawPdf()
  {
    let graf=new Graph();
    graf.SetDataPDF();
    DrawTxt.DrawTxtDatA("boxDat1A", graf );
    DrawTxt.DrawTxtDatB("boxDat1B", graf );
    DrawSvg.DrawSvgGraf("boxDat2",  graf );
    let cpm = graf.CPM();
    DrawTxt.DrawTxtCpm ("boxDat3",  graf, cpm );
    DrawSvg.DrawSvgCpm ("boxDat4",  graf, cpm );
  }

  static ClickRand()
  {
    let graf=new Graph();
    graf.SetRand(10);
    DrawTxt.DrawTxtDatA("boxDat1A", graf );
    DrawTxt.DrawTxtDatB("boxDat1B", graf );
    DrawSvg.DrawSvgGraf("boxDat2",  graf );
    let cpm = graf.CPM();
    DrawTxt.DrawTxtCpm ("boxDat3",  graf, cpm );
    DrawSvg.DrawSvgCpm ("boxDat4",  graf, cpm );
  }

  static ClickBox1A()
  {
    document.getElementById('btnBox1A').style.background='#343'
    document.getElementById('btnBox1B').style.background='#211'
    document.getElementById('boxDat1A').style.display='';
    document.getElementById('boxDat1B').style.display='none';
  }

  static ClickBox1B()
  {
    document.getElementById('btnBox1A').style.background='#211'
    document.getElementById('btnBox1B').style.background='#343'
    document.getElementById('boxDat1A').style.display='none';
    document.getElementById('boxDat1B').style.display='';
  }
}

function Init()
{ // funkcja uruchamiana przy starcie strony //
  document.onselectstart = function(){return false;};
  document.getElementById('btnRand').addEventListener('click',Click.ClickRand);
  document.getElementById('btnBox1A').addEventListener('click',Click.ClickBox1A);
  document.getElementById('btnBox1B').addEventListener('click',Click.ClickBox1B);
  Click.DrawPdf();
  Click.ClickBox1A();
}

Init();
