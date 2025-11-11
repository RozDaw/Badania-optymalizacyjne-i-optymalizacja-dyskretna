///////////////////////////////////////////////////////////
////                                                  /////
////  Interakcja strony ASTAR                         /////
////                                                  /////
///////////////////////////////////////////////////////////

class DATA
{ //
  constructor()
  {
    this.size= {x:20, y:30};
    this.Rand();
  }
  //
  Rand()
  {
    this.mapa=[];
    for(let x=0; x<this.size.x; x++)
    {
      this.mapa[x]=[]
      for(let y=0; y<this.size.y; y++)
      {
        let s=0;
        if(Math.random()<0.4) s=3;
        this.mapa[x][y]={stan:s, dist:0};
      }
    }
    //stan 0: nieobliczony
    //stan 1: obliczony otwarty
    //stan 2: obliczony zamkniety
    //stan 3: mur
    this.A={x:3,y:5}
    this.B={x:this.size.x-3,y:this.size.y-4}
    this.mapa[this.A.x][this.A.y]={stan:1,dist:0};
    this.mapa[this.B.x][this.B.y]={stan:0,dist:0};
    this.isEnd=0;
    this.pathDist='brak';
  }
  //
  Reset()
  {
    for(let x=0; x<this.size.x; x++)
    {
      for(let y=0; y<this.size.y; y++)
      {
        let s=this.mapa[x][y].stan;
        if(s==2||s==1) s=0;
        this.mapa[x][y]={stan:s, dist:0};
      }
    }
    this.mapa[this.A.x][this.A.y]={stan:1,dist:0};
    this.isEnd=0;
    this.pathDist='brak';
  }
  //
  CopyFrom(data)
  {
    this.size= {x:data.size.x, y:data.size.y};
    this.A= {x:data.A.x, y:data.A.y};
    this.B= {x:data.B.x, y:data.B.y};
    this.isEnd=data.isEnd;
    this.pathDist = data.pathDist;
    this.mapa= []
    for(let x=0; x<this.size.x; x++)
    { this.mapa[x]=[]
      for(let y=0; y<this.size.y; y++)
        this.mapa[x][y]={stan:data.mapa[x][y].stan, dist:data.mapa[x][y].dist};
    }
  }
  //
  Step(type)
  {
    let node = this.getNextNode(type);
    if(this.isEnd) return;
    this.mapa[node.x][node.y].stan=2;
    if(node.x==this.B.x&&node.y==this.B.y)
    { this.isEnd=1;
      this.pathDist = this.mapa[this.B.x][this.B.y].dist;
      return;
    };
    let delta = [ {x:-1,y:0,c:1}, {x:+1,y:0,c:1},{x:0,y:-1,c:1},{x:0,y:+1,c:1},
        {x:-1,y:-1,c:1.5},{x:-1,y:1,c:1.5},{x:1,y:-1,c:1.5},{x:1,y:1,c:1.5} ]
    let nodeDist = this.mapa[node.x][node.y].dist;
    for(let i=0;i<8;i++)
    { //sasiadujace pola
      let [x,y]= [node.x+delta[i].x,node.y+delta[i].y];
      if(x>=0 && x<this.size.x && y>=0 && y<this.size.y)
      { //pole w granicach mapy
        let dist=nodeDist+delta[i].c;
        if(this.mapa[x][y].stan==0)
        { //pierwsze obliczenia
          this.mapa[x][y]={stan:1, dist:dist,from:node}
        }
        if(this.mapa[x][y].stan==1 && this.mapa[x][y].dist>dist)
        { //relaksacja obliczeń
          this.mapa[x][y]={stan:1,dist:dist,from:node}
        }
      }
    }
  }
  //
  getNextNode(type)
  {
    //wyznacza nastepny node do analizy
    //jest nim otwarty node o najmniejszej wartości
    let next=[];
    let best={f:-1}
    for(let x=0; x<this.size.x;x++)
      for(let y=0; y<this.size.y;y++)
        if(this.mapa[x][y].stan==1)
        { let g= this.mapa[x][y].dist;
          let [dx,dy] = [Math.abs(this.B.x-x), Math.abs(this.B.y-y)];
          let h= dx+dy;
          let [minXY,maxXY] = [Math.min(dx,dy),Math.max(dx,dy)]
          h= minXY*1.5 + (maxXY-minXY)*1.0; //dla 8 kierunkow
          let f= g;
          if(type=='A') f= g+h;
          if(type=='H') f=h;
          if(best.f==-1 || f<best.f || (f==best.f&&h<best.h) )
             best={f:f,h:h,x:x,y:y}
        }
    if(best.f==-1) this.isEnd=2;
    return {x:best.x,y:best.y}
  }
}

dataA=new DATA()
dataB=new DATA()
dataC=new DATA()

dataB.CopyFrom(dataA)
dataC.CopyFrom(dataA)
timer=0;

class CANVAS
{ // wyświetlanie przy pomocy Canvas //
  static DrawData(can,data)
  { //rysuje na Box'ie graf
    let canvas = document.getElementById(can);
    let ctx = canvas.getContext("2d");
    this.#SetCanvasCtxSize(canvas,ctx,250+40,375+40);
    this.#DrawCtxData(ctx,data);
  }
  //
  static #SetCanvasCtxSize(canvas,ctx,width,height)
  { //ustawia aby 1px ctx był jednym pixelem ekranu
    var devicePixelRatio = window.devicePixelRatio || 1;
    canvas.width  =  width * devicePixelRatio;
    canvas.height =  height * devicePixelRatio;
    canvas.style.width  = width + 'px';
    canvas.style.height = height + 'px';
    ctx.scale(devicePixelRatio, devicePixelRatio)
  }

  static #DrawCtxData(ctx,data)
  { //dane svg:grid
    ctx.strokeStyle = '#271717'
    ctx.lineWidth = '1'
    let pad = 20;
    let sep = (290-2*pad) / data.size.x;
    ctx.beginPath();
    for(let a=0;a<=data.size.x;a++)
      { let x=sep*a+pad+0.5; ctx.moveTo(x,pad); ctx.lineTo(x,415-pad); }
    for(let b=0;b<=data.size.y;b++)
      { let y=sep*b+pad+0.5; ctx.moveTo(pad,y); ctx.lineTo(291-pad,y); }
    ctx.stroke();
    for(let a=0;a<data.size.x;a++)
    for(let b=0;b<data.size.y;b++)
    {
      let [x,y] = [pad+a*sep,pad+b*sep];
      if(data.mapa[a][b].stan==1)
      { //pole otwarte
        ctx.beginPath();
        ctx.strokeStyle = "#242";
        ctx.rect(x+1.5,y+1.5,sep-2,sep-2);
        ctx.stroke();
      }
      if(data.mapa[a][b].stan==2)
      { //pole zamkniete
        ctx.beginPath();
        ctx.fillStyle = "#242";
        ctx.fillRect(x+1,y+1,sep-1,sep-1);
        ctx.stroke();
      }
      if(data.mapa[a][b].stan==3)
      { //pole zabronione
        ctx.beginPath();
        ctx.fillStyle = "#222";
        ctx.fillRect(x+1,y+1,sep-1,sep-1);
        ctx.stroke();
      }
    }
    //path from B
    if(data.isEnd==1)
    {
      let pkt = data.B
      ctx.beginPath();
      //ctx.globalAlpha = 0.6;
      ctx.lineJoin = "round";
      ctx.strokeStyle = '#522'
      ctx.lineWidth = 8
      let [x,y] = [pad+pkt.x*sep+0.5+sep/2,pad+pkt.y*sep+0.5+sep/2];
      ctx.moveTo(x,y);
      while(pkt.x!=data.A.x || pkt.y!=data.A.y)
      {
        pkt = data.mapa[pkt.x][pkt.y].from;
        [x,y] = [pad+pkt.x*sep+0.5+sep/2,pad+pkt.y*sep+0.5+sep/2];
        ctx.lineTo(x,y);
      }
      ctx.stroke();
    }
    //AB
    ctx.beginPath();
    ctx.fillStyle = "#944";
    let [x,y] = [pad+data.A.x*sep,pad+data.A.y*sep];
    ctx.arc(x+sep/2+0.5,y+sep/2+0.5,sep/2-2,0,6.3);
    [x,y] = [pad+data.B.x*sep,pad+data.B.y*sep];
    ctx.arc(x+sep/2+0.5,y+sep/2+0.5,sep/2-2,0,6.3);
    ctx.fill();
  }
}

class ACTION
{ // zbiór funkcji: wywoływanych po kliknięciu //
  //
  static ClickRand()
  {
    clearTimeout(timer);
    ACTION.Rand();
    ACTION.Run();
  }
  //
  static ClickReset()
  {
    clearTimeout(timer);
    ACTION.Reset();
    ACTION.Run();
  }
  //
  static Rand()
  {
    dataA.Rand();
    dataB.CopyFrom( dataA );
    dataC.CopyFrom( dataA );
    ACTION.Reset();
  }
  //
  static Reset()
  {
    clearTimeout(timer);
    dataA.Reset();
    dataB.Reset();
    dataC.Reset();
    CANVAS.DrawData('canA',dataA);
    CANVAS.DrawData('canB',dataB);
    CANVAS.DrawData('canC',dataC);
    document.getElementById('txtA') .innerHTML= 'A*'
    document.getElementById('txtB') .innerHTML= 'Dijkstra'
    document.getElementById('txtC') .innerHTML= 'Heurystyka'
  }
  //
  static Run()
  {
    if(dataA.isEnd==0)
    { //dla <dataA> wykonuje krok i wyświetla
      dataA.Step('A');
      CANVAS.DrawData('canA',dataA);
      if(dataA.isEnd==1) document.getElementById('txtA') .innerHTML= 'A* ( dystans:'+dataA.pathDist.toFixed(1)+' )'
	  if(dataA.isEnd==2) document.getElementById('txtA') .innerHTML= 'A* ( brak ścieżki )'
    }
    if(dataB.isEnd==0)
    { //dla <dataA> wykonuje krok i wyświetla
      dataB.Step('D');
      CANVAS.DrawData('canB',dataB);
      if(dataB.isEnd==1)document.getElementById('txtB') .innerHTML='Dijkstra ( dystans:'+dataB.pathDist.toFixed(1)+' )'
	  if(dataB.isEnd==2)document.getElementById('txtB') .innerHTML='Dijkstra ( brak ścieżki )'
    }
    if(dataC.isEnd==0)
    { //dla <dataA> wykonuje krok i wyświetla
      dataC.Step('H');
      CANVAS.DrawData('canC',dataC);
      if(dataC.isEnd==1) document.getElementById('txtC') .innerHTML='Heurystyka ( dystans:'+dataC.pathDist.toFixed(1)+' )'
	  if(dataC.isEnd==2) document.getElementById('txtC') .innerHTML='Heurystyka ( brak ścieżki )'
    }
    if(dataA.isEnd==0 || dataB.isEnd==0 || dataC.isEnd==0 )
      timer=setTimeout(ACTION.Run,20);
  }
  //
}

function main()
{ // funkcja uruchamiana przy starcie strony //
  document.onselectstart = function(){return false;};
  document.getElementById('btnRand') .addEventListener('click',ACTION.ClickRand);
  document.getElementById('btnReset').addEventListener('click',ACTION.ClickReset);
  CANVAS.DrawData('canA',dataA)
  CANVAS.DrawData('canB',dataB)
  CANVAS.DrawData('canC',dataC)
  ACTION.Run();
}

main();
