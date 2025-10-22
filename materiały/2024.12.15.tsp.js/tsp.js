/*
  W programie są dwie zmienne:
    tspData: zmienna przechowywująca dane problemu
    logData: zmienna przechowywująca log z kolejnych kroków algorytmu
             obliczana jest 1 zaraz po wygenerowaniu nowej instancji,
             animacja itp leci już z <logData> nic nie liczy
  oraz klasy (zbiory statycznych funkcji)
    SA: klasa dostarcza <logData> dla algorytmu symulowanego wyżarzania
    CANVAS: klasa rysująca <logData> na stronie
    ACTION: klasa zawierająca metody interfejsu
*/

class TSPDATA
{ //dane tsp
  SetRand()
  { //ustawia losowo wierzchołki odległe od siebie o co najmniej 2
    let nodeN=40;
    this.nodes=[];
    for(let i=0;i<nodeN;)
    {
      let [x,y]=[Math.floor(Math.random()*100), Math.floor(Math.random()*50)]
      let ok=1;
      if (x+2*y<25) ok=0; // odciety trójkąt na opis
      for(let i=0;i<this.nodes.length;i++)
      {
        let dx = (x-this.nodes[i].x);
        let dy = (y-this.nodes[i].y);
        if (dx*dx+dy*dy<4) ok=0;
      }
      if(ok==1){i++;this.nodes.push({x:x,y:y});}
    }
  }
  GetEdgeDist(a,b)
  { //podaje odleglość pomiędzy wierzchołkami o indeksach <a> i <b>
    let [dx,dy] = [this.nodes[a].x-this.nodes[b].x,
                   this.nodes[a].y-this.nodes[b].y];
    return Math.floor(0.5+Math.sqrt(dx*dx+dy*dy))
  }
  GetPathDist(path)
  { //podaje długość ścieżki <path>
    let length=0;
    for(let i=1;i<path.length;i++)
      length += this.GetEdgeDist( path[i-1],path[i] );
    return length;
  }
  GetNodeXY(id)
  { //podaje współrzędne wierzchoł
	  return{ x: 8*this.nodes[id].x, y:8*this.nodes[id].y }
  }
}

class A123
{
  static GetLogRun(data)
  {
    let path=[];
    for(let i=0;i<data.nodes.length;i++) path.push(i);
    path.push(0);
    return [ {}, {dist:data.GetPathDist(path), path:path} ];
  }
}

class NN
{ //algorytm najbliższego sąsiada (ang. nearest neighbour)
  static GetLogRun(data)
  { //funkcja zwracająca <log> z działania alogrytmu
    let path= NN.GetStartPath(data);
    let log= [ {}, {dist:0, path:path} ];
    for(let n=0; n<data.nodes.length;n++)
    { path = NN.GetNextPath( data,path,1 );
      log.push( {dist:data.GetPathDist(path),path:path} )
    }
    return log;
  }
  static GetStartPath(data)
  { //zwraca startową scieżkę
    //1 wierzchołek o numerze 0
    return [ 0 ]
    //return [ Math.floor(Math.random()*data.nodes.length) ]
  }
  static GetNextPath(data,path,stepN)
  { //zwraca sciezke po wykonaniu na <path> <stepN> kroków algorytmu NN
    let nextpath = Array.from(path);
    let inpath = new Array(data.nodes.length);
    for(let i=0;i<data.nodes.length;i++) inpath[i]=0;
    for(let i=0;i<path.length;i++) inpath[nextpath[i]]=1;
    for(let step=0;step<stepN;step++)
    {
      let node=nextpath[nextpath.length-1];
      let next=-1,distTmp=0;
      for(let i=0;i<data.nodes.length;i++)if(inpath[i]==0)
        if(next==-1||data.GetEdgeDist(node,i)<distTmp)
          {next=i;distTmp=data.GetEdgeDist(node,i);}
      if(next==-1){nextpath.push(nextpath[0]);break;}
      nextpath.push(next);
      inpath[next]=1;
    }
    return nextpath
  }
}

class FI
{ //algorytm wstawiania najdalszego (ang.Farthest Insertion)
  static GetLogRun(data)
  { //funkcja zwracająca <log> z działania alogrytmu
    let path= FI.GetStartPath(data);
    let log= [ {}, {dist:0, path:path} ];
    for(let n=0; n<data.nodes.length;n++)
    { path = FI.GetNextPath( data,path,1 );
      log.push( {dist:data.GetPathDist(path),path:path} )
    }
    return log;
  }
  static GetStartPath(data)
  { //zwraca startową ścieżkę
    //cykl składającą się z 1 pary najbardziej oddalnych od siebie wierzchołków
    let dist=0, a=0, b=0;
    for(let i=0;i<data.nodes.length;i++)
      for(let k=0;k<data.nodes.length;k++)
        if(data.GetEdgeDist(i,k)>dist){a=i;b=k;dist=data.GetEdgeDist(i,k);}
    return [a,b,a];
  }
  static GetNextPath(data,path,stepN)
  { //zwraca cykl po wykonaniu na <path> <stepN> kroków algorytmu FI
    {//deklaracja i inicjalizacja zmienych <cycle><dist><start>
      var start = path[0];
      var cycle = new Array( data.nodes.length );
      var dist  = new Array( data.nodes.length );
      for(let i=0;i<data.nodes.length;i++) cycle[i]=-1;
      for(let i=0;i<data.nodes.length;i++) dist[i]=data.GetEdgeDist(start,i);
      for(let i=1;i<path.length;i++) cycle[path[i-1]]=path[i];
      for(let i=0;i<data.nodes.length;i++)if(cycle[i]==-1)
        for(let k=0;k<data.nodes.length;k++)if(cycle[k]!=-1)
          dist[i]=Math.min(dist[i],data.GetEdgeDist(i,k));
    }
    {//dodawanie kolejnych wierzchołów do cyklu
      var idStart=path.length-1, idStop=Math.min(data.nodes.length,idStart+stepN);
      for(let i=idStart;i<idStop;i++)
      {
        {//wybór najdalszego wierzchołka <next>
          let maxdist=-1;
          var next=-1;
          for(let j=0;j<data.nodes.length;j++)
            if(cycle[j]==-1&&dist[j]>maxdist){maxdist=dist[j];next=j;}
          //???if(next==-1){path.add(path.get(0));break;}
        }
        {//wybór najlepszej pozycji <pos> dla nowego wierzchołka <next>
          var pos=start;
          let cost=0,tcost=0,k=start;
          for(let j=0;j<i;j++)
          { let k2=cycle[k];
            tcost = data.GetEdgeDist(k,next)+data.GetEdgeDist(next,k2)-data.GetEdgeDist(k,k2);
            if((j==0)||(tcost<cost)){cost=tcost;pos=k;}
            k=k2;
          }
        }
        {//dodanie do cyklu <cycle> wierzchołka <next> na pozycje <pos>
          cycle[next]=cycle[pos];
          cycle[pos]=next;
          for(let j=0;j<data.nodes.length;j++)
            if(cycle[j]==-1)dist[j]=Math.min(dist[j],data.GetEdgeDist(next,j));
        }
      }
    }
    {//utworzenie ścieżki <nextpath> na podstawie <cycle>
      var nextpath=[];
      for(let k=start,i=0;i<=idStop;i++,k=cycle[k])
        nextpath.push(k);
    }
    return nextpath;
  }
}

class TO
{ // algorytm popraw dwu-optymalny
  static SetLogRun(logData,data)
  { //funkcja zwracająca <log> z działania alogrytmu
    let oldDist= 0;
    let path= logData[logData.length-1].path;
    let dist= logData[logData.length-1].dist;
    while(oldDist!=dist)
    { oldDist = dist;
      logData.push( {dist:dist,path:path} )
      path = TO.GetNextPath( data,path,1 );
      dist = data.GetPathDist( path );
    }
  }
  static GetNextPath(data,path,step)
  { //zwraca cykl po wykonaniu na <path> <stepN> kroków algorytmu FI
    let nextpath = Array.from(path)
    for(let n=0;n<step;n++)
    {
      let bestLeft=0, bestRight=0, bestDelta=0;
      for(let a=0;a<data.nodes.length;a++)for(let b=a+1;b<data.nodes.length;b++)
      {
        let [a0,a1] = [nextpath[a], nextpath[a+1]];
        let [b0,b1] = [nextpath[b] ,nextpath[b+1]];
        /* ----(a0)---(a1)-----      ----(a0)   (a1)-----
          |                    |    |         x          |
           ----(b1)---(b0)-----      ----(b1)  (b0)------
        */
        let delta = +data.GetEdgeDist(a0,b0)+data.GetEdgeDist(a1,b1)
                    -data.GetEdgeDist(a0,a1)-data.GetEdgeDist(b0,b1)
        if(delta<bestDelta)[bestDelta,bestLeft,bestRight]=[delta,a+1,b]
      }
      if(bestDelta<0)
      { //odwracanie
        while(bestRight>bestLeft)
        { [nextpath[bestLeft],nextpath[bestRight]]
           =[nextpath[bestRight],nextpath[bestLeft]]
          bestLeft+=1; bestRight-=1;
        }
      }
    }
    return nextpath;
  }
}

class SA
{ //algorytm symulowanego wyżarzania
  static GetLogRun(tsp)
  { //wykonuje algorytm SA: zwraca <log>
    let temp = 20;                        // początkowa temperatura
    let path = SA.GetStartPath(tspData);  // początkowa ścieżka
    let dist = tsp.GetPathDist(path);     // długość początkowej scieżki
    let best = {dist:dist, path:path};    // najlepsze znalezione rozwiązanie
    let log  = [                          // log z pracy algorytmu
      {},                                 // log[0]: rysuje tylko dane tsp
      {dist:dist, path:path, temp:temp}]; // log[1]: tylko parametry startowe
    for(let n=0; n<400; n++)
    {
      temp = temp * 0.99;
      SA.SetLogStep( {log:log, tsp:tsp, best:best, temp:temp, stepN:100} );
    }
    best.temp = temp;
    log.push(best);
    return log;
  }
  static SetLogStep(input)
  { //wykonuje jeden etap algorytmu: modyfikuje <input.log, input.best>
    let path = Array.from( input.log[input.log.length-1].path )
    let c0 = input.tsp.GetPathDist(path);
    let praw=0,akce=0,delta=0;
    for(let i=0; i<input.stepN; i++)
    {
      let move = SA.GetRandAB(input.tsp.nodes.length);
      SA.SetPathMove( path, move );
      var c1 = input.tsp.GetPathDist(path);
      if(c1<input.best.dist){input.best.dist=c1;input.best.path=Array.from(path);}
      if(c1>c0)
      { delta=c1-c0;
        praw = Math.exp( (c0-c1)/input.temp );
        akce = ( Math.random()<praw );
      }
      if(c1<=c0||akce)  c0=c1; //akceptuje ruch
      else SA.SetPathMove( path,move ); //odrzucenie ruchu
    }
    input.log.push( {dist:c0,path:path,temp:input.temp,praw:praw,akce:akce,delta:delta} );
  }
  static GetStartPath(tsp)
  { //zwraca zinicjowanie algorytmu: <dist,path,temp>
    let path=[];
    for(let i=0;i<tsp.nodes.length;i++) path.push(i); path.push(0);
    return path;
  }
  static GetRandAB(size)
  { //losuje pare różnch liczb <A,B> z przedziału [1,size-1]
    var a=1+Math.floor(Math.random()*(size-1));
    var b=1+Math.floor(Math.random()*(size-2)); if(b>=a)b++;
    if(a>b) [a,b]=[b,a];
    return [a,b];
  }
  static SetPathMove(path,move)
  { //dokonuje zamiany <move> na ścieżce <path>
    var a=move[0], b=move[1];
    while(a<b){[path[a],path[b]]=[path[b],path[a]]; a++;b--;}
  }
}

class CANVAS
{ // wyświetlanie przy pomocy Canvas //
  static Init()
  { //ustawia parametry canvasów
    let width = 900
    let height = 440;
    let devicePixelRatio = window.devicePixelRatio || 1;
    for(let i=0;i<1;i++ )
    { let can = ['canPath'][i];
      let canvas = document.getElementById(can);
      let ctx = canvas.getContext("2d");
      canvas.width  =  width * devicePixelRatio;
      canvas.height =  height * devicePixelRatio;
      canvas.style.width  = width + 'px';
      canvas.style.height = height + 'px';
      ctx.scale(devicePixelRatio, devicePixelRatio)
    }
  }
  static Update(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canPath');
    let ctx = canvas.getContext("2d");
    let path = logData[frame].path;
    let nextId=frame+1;
    if(nextId==logData.length)nextId-=1;
    if(frame==0)nextId=0;
    let nextpath = logData[nextId].path;

    //siatka
    { //rysuje tlo pod rysunki (3xsiatka)
      ctx.beginPath();
      ctx.fillStyle = "#211";
      ctx.fillRect(0,0,900,440);
      ctx.fill();
      ctx.strokeStyle = '#251515'; ctx.lineWidth = '1';
      CANVAS.#CtxDrawGrid(ctx,{marginX:50,marginY:20,sizeX:800,sizeY:400,nX:100,nY:50,rX:8,rY:8});
      ctx.strokeStyle = '#281818'; ctx.lineWidth = '1';
      CANVAS.#CtxDrawGrid(ctx,{marginX:50,marginY:20,sizeX:800,sizeY:400,nX:20,nY:10,rX:8,rY:8});
      ctx.strokeStyle = '#2a1a1a'; ctx.lineWidth = '1';
      CANVAS.#CtxDrawGrid(ctx,{marginX:50,marginY:20,sizeX:800,sizeY:400,nX:10,nY:5,rX:10,rY:10});
    }
    //sciezka
    if(path)
    {
      ctx.beginPath();
      ctx.strokeStyle = '#464'
      ctx.lineWidth = '6'
      ctx.lineJoin = "round";
      for(let i=0; i<path.length; i++)
      {
        let axy = tspData.GetNodeXY( path[i] );
        let [eX,eY] = [50.5+axy.x, 20.5+axy.y]
        if(i==0) ctx.moveTo(eX,eY)
        else ctx.lineTo(eX,eY)
      }
      ctx.stroke();
    }

    //wierzchołki
    let nodeType = new Array(tspData.nodes.length);
    for(let i=0;i<tspData.nodes.length;i++)nodeType[i]=0;
    if(nextpath)
      for(let i=0;i<nextpath.length;i++)nodeType[nextpath[i]]=2;
    if(path)
      for(let i=0;i<path.length;i++)nodeType[path[i]]=1;


    //znikające krawędzie
    ctx.beginPath();
    ctx.strokeStyle = '#322'
    ctx.lineWidth = '3'
    ctx.lineJoin = "round";
    if(nextpath!==undefined)
    for(let i=0; i<path.length-1; i++)
    {
      let a= path[i];
      let b= path[i+1];
      let isone=1;
      for(let i=0; i<nextpath.length-1; i++)
        if((a==nextpath[i]&&b==nextpath[i+1])||(a==nextpath[i+1]&&b==nextpath[i]))isone=0;
      if(isone==1)
      {
        let axy = tspData.GetNodeXY(a);
        let bxy = tspData.GetNodeXY(b);
        let [eaX,eaY] = [50.5+axy.x, 20.5+axy.y]
        let [ebX,ebY] = [50.5+bxy.x, 20.5+bxy.y]
        ctx.moveTo(eaX,eaY)
        ctx.lineTo(ebX,ebY)
      }
    }
    ctx.stroke();

    //pojawiające się krawędzie
    ctx.beginPath();
    ctx.strokeStyle = '#322'
    ctx.lineWidth = '3'
    ctx.lineJoin = "round";
    if(nextpath!==undefined)
    for(let i=0; i<nextpath.length-1; i++)
    {
      let a= nextpath[i];
      let b= nextpath[i+1];
      let isone=1;
      for(let i=0; i<path.length-1; i++)
        if((a==path[i]&&b==path[i+1])||(a==path[i+1]&&b==path[i]))isone=0;
      if(isone==1)
      {
        let axy = tspData.GetNodeXY(a);
        let bxy = tspData.GetNodeXY(b);
        let [eaX,eaY] = [50.5+axy.x, 20.5+axy.y]
        let [ebX,ebY] = [50.5+bxy.x, 20.5+bxy.y]
        ctx.moveTo(eaX,eaY)
        ctx.lineTo(ebX,ebY)
      }
    }
    ctx.stroke();

    //węzły
    ctx.strokeStyle = '#343'
    ctx.fillStyle = '#343';
    ctx.lineWidth = '2'
    for(let i=0;i<tspData.nodes.length;i++)
    {
      ctx.beginPath();
      let xy = tspData.GetNodeXY(i);
      let [eX,eY] =[50+xy.x, 20+xy.y]
      if(nodeType[i]==0) {ctx.arc(eX,eY,5,0,6.3);ctx.stroke();}
      if(nodeType[i]==1) {ctx.arc(eX,eY,6,0,6.3);ctx.fill();ctx.stroke();}
      if(nodeType[i]==2)
      { ctx.arc(eX,eY,5,0,6.3);ctx.stroke();
        ctx.beginPath();ctx.arc(eX,eY,8,0,6.3);ctx.stroke();
      }
    }
    //path length
    if(frame>0)
    {
      ctx.font = "16px Courier";ctx.fillStyle = '#666'
      ctx.fillText( 'długość: '+logData[frame].dist,52,38);
    }
  }
  static #CtxDrawGrid(ctx,grid)
  { //rysuje siatke na <ctx>, parametry siatki to <grid>
    ctx.beginPath();
    for(let a=0;a<=grid.nX;a++)
    { let x=0.5+grid.marginX+grid.sizeX*a/grid.nX;
      let y0=0.5+grid.marginY-grid.rY;
      let y1=0.5+grid.marginY+grid.sizeY+grid.rY
      ctx.moveTo(x,y0); ctx.lineTo(x,y1);
    }
    for(let b=0;b<=grid.nY;b++)
    { let y=0.5+grid.marginY+grid.sizeY*b/grid.nY;
      let x0=0.5+grid.marginX-grid.rX;
      let x1=0.5+grid.marginX+grid.sizeX+grid.rX;
      ctx.moveTo(x0,y); ctx.lineTo(x1,y);
    }
    ctx.stroke();
  }
}

class ACTION
{ // zbiór funkcji: wywoływanych po kliknięciu //
  //
  static ClickRand()
  {
    clearTimeout(timer);
    tspData.SetRand();
    slider.value='0';
    slider.max='0';
    CANVAS.Update(0);
  }
  //
  static ClickA123()
  {
    clearTimeout(timer);
    logData = A123.GetLogRun( tspData );
    slider.max= logData.length-1;
    slider.value='0';
    ACTION.Loop();
  }
  //
  static ClickNN()
  {
    clearTimeout(timer);
    logData = NN.GetLogRun( tspData );
    slider.max= logData.length-1;
    slider.value='0';
    ACTION.Loop();
  }
  //
  static ClickFI()
  {
    clearTimeout(timer);
    logData = FI.GetLogRun( tspData );
    slider.max= logData.length-1;
    slider.value='0';
    ACTION.Loop();
  }
  //
  static ClickTO()
  {
    clearTimeout(timer);
    slider.value= logData.length-1;
    TO.SetLogRun( logData,tspData );
    slider.max= logData.length-1;
    ACTION.Loop();
  }
  //
  static ClickSA()
  {
    clearTimeout(timer);
    logData = SA.GetLogRun( tspData );
    slider.max= logData.length-1;
    slider.value='0';
    ACTION.Loop();
  }
  //
  static ClickReport()
  {
    //data
    let text = 'data:\n'
    text += tspData.nodes.length+'\n';
    for(let i=0; i<tspData.nodes.length; i++)
    { text += tspData.nodes[i].x.toString().padStart(2,' ')+' '
            + tspData.nodes[i].y.toString().padStart(2,' ')+'   ';
    }
    text += '\n';
    //path
    text += '\nstep : length : path\n'
    for(let n=1; n<logData.length; n++)
    {
      let dist = logData[n].dist;
      let path = logData[n].path;
      text += n.toString().padStart(4,' ')+' : '
              +dist.toString().padStart(6,' ')+' : ';
      for(let i=0; i<path.length; i++)
      text += path[i]+' ';
      text += ' \n';
    }
    ACTION.NewWindowData(text);
  }
  //
  static ClickSlider(value)
  {
    clearTimeout(timer);
    value = parseInt(value)
    CANVAS.Update(value)
  }
  //
  static Loop()
  {
    let frame = parseInt(slider.value)
    if(frame==slider.max)
      CANVAS.Update(frame);
    if(frame<slider.max)
    {
      frame +=1;
      slider.value = frame;
      CANVAS.Update(frame);
      if(frame<slider.max)
       timer=setTimeout(ACTION.Loop,20 );
    }
  }
  //
  static NewWindowData(data)
  { var blob = new Blob([data], {type:"text/plain"});
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    window.open(link)
    URL.revokeObjectURL(url);
  }
  //
  static Key(key)
  {
    var el = document.getElementById('txtA');
    if(key.code=="ArrowRight")
    {
      let frame = parseInt(slider.value)+1;
      if(frame<logData.length)
      { slider.value = frame;
        CANVAS.Update(frame);
      }
    }
    if(key.code=="ArrowLeft")
    {
      let frame = parseInt(slider.value)-1;
      if(frame>=0)
      { slider.value = frame;
        CANVAS.Update(frame);
      }
    }
  }
}

{ // MAIN: funkcja uruchamiana przy starcie strony //
  timer=0;
  logData=[{}]
  tspData=new TSPDATA()
  document.onselectstart = function(){return false;};
  document.getElementById('btnRand'  ).addEventListener('click',ACTION.ClickRand);
  document.getElementById('btnA123'  ).addEventListener('click',ACTION.ClickA123);
  document.getElementById('btnNN'    ).addEventListener('click',ACTION.ClickNN );
  document.getElementById('btnFI'    ).addEventListener('click',ACTION.ClickFI );
  document.getElementById('btnTO'    ).addEventListener('click',ACTION.ClickTO );
  document.getElementById('btnSA'    ).addEventListener('click',ACTION.ClickSA );
  document.getElementById('btnReport').addEventListener('click',ACTION.ClickReport);
  document.addEventListener("keydown", ACTION.Key);
  var slider = document.getElementById("slider");
  slider.oninput = function(){ACTION.ClickSlider(this.value);}
  CANVAS.Init();
  ACTION.ClickRand();
}
