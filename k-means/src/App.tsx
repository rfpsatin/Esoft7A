import React, { useState, useRef, useEffect, useMemo } from 'react';
import { Point } from './types';
import { calculateCentroid, findNearestCluster, calculateEuclideanDistance } from './utils/distance';
import { CircleDot, Trash2, Plus, Minus, RefreshCw, HelpCircle } from 'lucide-react';
import { categoricalToNumeric } from './utils/distance';

function App() {
  const [points, setPoints] = useState<Point[]>([]);
  const [clusters, setClusters] = useState<Point[]>([]);
  const [numClusters, setNumClusters] = useState(2);
  const [isRunning, setIsRunning] = useState(false);
  const [showHelp, setShowHelp] = useState(true);
  const [popupStep, setPopupStep] = useState(0);
  const [showPopup, setShowPopup] = useState(true);
  const [popupShown, setPopupShown] = useState(false);
  const [dispersionThreshold, setDispersionThreshold] = useState(120);
  const [showDispersionTutorial, setShowDispersionTutorial] = useState(false);
  const [categoricalValue, setCategoricalValue] = useState('');
  const [showKnnTutorial, setShowKnnTutorial] = useState(false);
  const [lastCategorical, setLastCategorical] = useState('');
  const [lastNumericValue, setLastNumericValue] = useState<number | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const colors = useMemo(() => [
    '#FF6B6B',
    '#4ECDC4', 
    '#45B7D1',
    '#96CEB4',
    '#FFEEAD',
    '#D4A5A5',
    '#9B59B6',
    '#3498DB'
  ], []);

  const CANVAS_WIDTH = 800;
  const CANVAS_HEIGHT = 600;

  useEffect(() => {
    drawCanvas();
  }, [points, clusters]);

  const drawCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= canvas.width; i += 50) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, canvas.height);
      ctx.stroke();
    }
    for (let i = 0; i <= canvas.height; i += 50) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(canvas.width, i);
      ctx.stroke();
    }

    if (clusters.length > 0) {
      for (let x = 0; x < canvas.width; x += 10) {
        for (let y = 0; y < canvas.height; y += 10) {
          const point = { x, y, id: '', clusterId: 0, isCentroid: false };
          const clusterId = findNearestCluster(point, clusters);
          ctx.fillStyle = `${colors[clusterId % colors.length]}55`;
          ctx.fillRect(x, y, 10, 10);
        }
      }
    }

    points.forEach((point) => {
      ctx.beginPath();
      ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI);
      ctx.fillStyle = colors[point.clusterId % colors.length];
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    clusters.forEach((centroid, index) => {
      ctx.beginPath();
      ctx.arc(centroid.x, centroid.y, 8, 0, 2 * Math.PI);
      ctx.fillStyle = colors[index % colors.length];
      ctx.fill();
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.font = '14px Arial';
      ctx.fillStyle = '#000';
      ctx.textAlign = 'center';
      ctx.fillText(`C${index + 1}`, centroid.x, centroid.y - 15);
    });
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current || isRunning) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const newPoint: Point = {
      id: `point-${Date.now()}`,
      x,
      y,
      clusterId: clusters.length > 0 ? findNearestCluster({ x, y } as Point, clusters) : 0,
      isCentroid: false,
    };

    setPoints([...points, newPoint]);
    setShowHelp(false);
    if (!popupShown && points.length === 0) {
      setPopupStep(1);
      setShowPopup(true);
      setPopupShown(true);
    }
  };

  const initializeClusters = () => {
    if (points.length < numClusters) {
      alert('Adicione mais pontos antes de inicializar os grupos!');
      return;
    }

    const shuffled = [...points].sort(() => 0.5 - Math.random());
    const initialCentroids = shuffled.slice(0, numClusters).map((point, index) => ({
      ...point,
      clusterId: index,
      isCentroid: true,
    }));

    setClusters(initialCentroids);

    const updatedPoints = points.map((point) => ({
      ...point,
      clusterId: findNearestCluster(point, initialCentroids),
    }));

    setPoints(updatedPoints);
  };

  const analyzeDispersionAndSplit = () => {
    let moved = false;
    let newClusters = [...clusters];
    let newPoints = [...points];
    let nextClusterId = clusters.length;
    clusters.forEach((centroid) => {
      const clusterPoints = newPoints.filter(p => p.clusterId === centroid.clusterId && !p.isCentroid);
      const distantPoints = clusterPoints.filter(p => calculateEuclideanDistance(p, centroid) > dispersionThreshold);
      if (distantPoints.length > 0) {
        moved = true;
        const newCentroid = calculateCentroid(distantPoints);
        newCentroid.clusterId = nextClusterId;
        newCentroid.isCentroid = true;
        newClusters.push(newCentroid);
        newPoints = newPoints.map(p =>
          distantPoints.includes(p) ? { ...p, clusterId: nextClusterId } : p
        );
        nextClusterId++;
      }
    });
    if (moved) {
      setClusters(newClusters);
      setPoints(newPoints);
      setShowDispersionTutorial(true);
    }
  };

  const runKMeans = () => {
    if (clusters.length === 0) {
      initializeClusters();
      return;
    }

    setIsRunning(true);
    const interval = setInterval(() => {
      const newCentroids = clusters.map((_, index) => {
        const clusterPoints = points.filter((p) => p.clusterId === index);
        return calculateCentroid(clusterPoints);
      });

      const updatedPoints = points.map((point) => ({
        ...point,
        clusterId: findNearestCluster(point, newCentroids),
      }));

      setClusters(newCentroids);
      setPoints(updatedPoints);
    }, 500);

    setTimeout(() => {
      clearInterval(interval);
      setIsRunning(false);
      analyzeDispersionAndSplit();
    }, 3000);
  };

  const handleClearPoints = () => {
    setPoints([]);
    setClusters([]);
  };

  const popups = [
    {
      title: 'O que é um Cluster?',
      text: 'Um cluster é um grupo de pontos que possuem características parecidas. Aqui, cada grupo será representado por uma cor diferente. Experimente adicionar mais pontos!'
    },
    {
      title: 'Como funciona?',
      text: 'O algoritmo K-means agrupa os pontos de acordo com a proximidade. Cada grupo tem um centroide (círculo maior), que é o “coração” do grupo. Você pode ajustar o número de grupos e ver como os pontos se organizam!'
    },
    {
      title: 'Na prática',
      text: 'Clusters são usados para segmentar clientes, identificar padrões e muito mais. Clique em "Agrupar Pontos" para ver a mágica acontecer!'
    }
  ];

  const helpText = (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">🎮 Como Brincar com os Grupos</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="flex items-center gap-2 font-semibold mb-2">
            <CircleDot className="w-5 h-5" /> Adicionar Pontos
          </p>
          <p className="text-sm">Como colocar bolinhas de gude no chão - clique onde quiser!</p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="flex items-center gap-2 font-semibold mb-2">
            <Plus className="w-5 h-5" />/<Minus className="w-5 h-5" /> Ajustar Grupos
          </p>
          <p className="text-sm">Como decidir quantas equipes terá na brincadeira</p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="flex items-center gap-2 font-semibold mb-2">
            <RefreshCw className="w-5 h-5" /> Agrupar
          </p>
          <p className="text-sm">Como mágica, os pontos se organizam em times!</p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="flex items-center gap-2 font-semibold mb-2">
            <Trash2 className="w-5 h-5" /> Recomeçar
          </p>
          <p className="text-sm">Como limpar o quadro para começar de novo</p>
        </div>
      </div>
      <div className="mt-4 bg-yellow-50 p-4 rounded-lg">
        <h3 className="font-semibold mb-2">🎨 O Significado das Cores:</h3>
        <p className="text-sm">
          • Cada cor é como um time diferente<br/>
          • Os círculos grandes (⭕) são como os capitães dos times<br/>
          • Os círculos pequenos (●) são os jogadores do time
        </p>
      </div>
    </div>
  );

  const dispersionTutorial = (
    <div className="absolute left-1/2 -translate-x-1/2 top-10 z-50 bg-white border border-pink-300 shadow-xl rounded-xl p-6 max-w-md flex flex-col items-center animate-fade-in">
      <h2 className="text-lg font-bold mb-2 text-pink-700">🎉 Novo Grupo Formado!</h2>
      <div className="mb-4 text-center space-y-4">
        <p className="text-gray-700">
          <span className="font-semibold">É como em uma festa quando...</span>
        </p>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-pink-50 p-3 rounded-lg">
            <p>👥 Um grupo de amigos</p>
            <p>começou falando de trabalho...</p>
          </div>
          <div className="bg-pink-50 p-3 rounded-lg">
            <p>💡 Mas alguns começaram</p>
            <p>a falar de hobbies...</p>
          </div>
          <div className="bg-pink-50 p-3 rounded-lg">
            <p>🔄 Naturalmente, eles</p>
            <p>formaram uma nova rodinha!</p>
          </div>
          <div className="bg-pink-50 p-3 rounded-lg">
            <p>✨ Assim nosso algoritmo</p>
            <p>cria novos grupos também!</p>
          </div>
        </div>
      </div>
      <button
        className="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600"
        onClick={() => setShowDispersionTutorial(false)}
      >Legal, Entendi!</button>
    </div>
  );

  const knnTutorial = (
    <div className="absolute left-1/2 -translate-x-1/2 top-24 z-50 bg-white border border-green-300 shadow-xl rounded-xl p-6 max-w-md flex flex-col items-center animate-fade-in">
      <h2 className="text-lg font-bold mb-2 text-green-700">🔄 Convertendo Texto em Números</h2>
      <div className="mb-4 text-center space-y-4">
        <p className="text-gray-700">
          É como dar notas para características:
        </p>
        <div className="bg-green-50 p-4 rounded-lg space-y-3">
          <div className="flex items-center justify-between">
            <span>📝 Seu texto: </span>
            <span className="font-bold">{lastCategorical || 'Exemplo'}</span>
          </div>
          <div className="flex items-center justify-center">
            <span className="text-2xl">⬇️</span>
          </div>
          <div className="flex items-center justify-between">
            <span>🔢 Virou o número: </span>
            <span className="font-bold text-green-600">{lastNumericValue}</span>
          </div>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          Como classificar filmes por gênero:<br/>
          "Ação" ➡️ 1<br/>
          "Comédia" ➡️ 2<br/>
          "Drama" ➡️ 3
        </p>
      </div>
      <button
        className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        onClick={() => setShowKnnTutorial(false)}
      >Agora Entendi!</button>
    </div>
  );

  const handleAddCategoricalPoint = () => {
    if (!categoricalValue.trim()) return;
    const numericValue = categoricalToNumeric(categoricalValue);
    setLastCategorical(categoricalValue);
    setLastNumericValue(numericValue);
    const newPoint: Point = {
      id: `cat-point-${Date.now()}`,
      x: Math.random() * 700 + 50,
      y: Math.random() * 500 + 50,
      clusterId: clusters.length > 0 ? findNearestCluster({ x: 0, y: 0 } as Point, clusters) : 0,
      isCentroid: false,
      originalValue: categoricalValue,
      numericValue,
    };
    setPoints([...points, newPoint]);
    setCategoricalValue('');
    if (!points.some(p => p.originalValue)) {
      setShowKnnTutorial(true);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="bg-white rounded-lg p-6 shadow-lg relative">
          {showDispersionTutorial && dispersionTutorial}
          {showKnnTutorial && knnTutorial}
          {/* Pop-up explicativo */}
          {showPopup && popupStep < popups.length && (
            <div className="absolute left-1/2 -translate-x-1/2 top-2 z-50 bg-white border border-blue-300 shadow-xl rounded-xl p-6 max-w-md flex flex-col items-center animate-fade-in">
              <h2 className="text-lg font-bold mb-2 text-blue-700">{popups[popupStep].title}</h2>
              <p className="text-gray-700 mb-4 text-center">{popups[popupStep].text}</p>
              <button
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                onClick={() => {
                  if (popupStep < popups.length - 1) {
                    setPopupStep(popupStep + 1);
                  } else {
                    setShowPopup(false);
                  }
                }}
              >
                {popupStep < popups.length - 1 ? 'Próximo' : 'Entendi!'}
              </button>
            </div>
          )}

          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold text-gray-800">Visualização de Clusters K-means</h1>
            <button
              onClick={() => setShowHelp(!showHelp)}
              className="text-gray-600 hover:text-gray-800"
              title="Ajuda"
            >
              <HelpCircle className="w-6 h-6" />
            </button>
          </div>
          
          {showHelp && (
            <div className="mb-6 p-4 bg-blue-50 rounded-lg text-gray-700">
              {helpText}
            </div>
          )}

          <div className="flex flex-col items-center space-y-4">
            <div className="relative">
              <canvas
                ref={canvasRef}
                width={CANVAS_WIDTH}
                height={CANVAS_HEIGHT}
                onClick={handleCanvasClick}
                className="border border-gray-200 rounded-lg cursor-crosshair bg-white"
              />
              <div className="absolute top-4 left-4 text-sm text-gray-500">
                Clique para adicionar pontos
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => handleClearPoints()}
                className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
                disabled={isRunning || points.length === 0}
              >
                <Trash2 className="w-5 h-5" />
                Limpar Pontos
              </button>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setNumClusters(Math.max(2, numClusters - 1))}
                  className="p-2 bg-gray-200 rounded-lg hover:bg-gray-300 disabled:opacity-50"
                  disabled={isRunning || numClusters <= 2}
                >
                  <Minus className="w-5 h-5" />
                </button>
                <span className="text-lg font-medium w-8 text-center">{numClusters}</span>
                <button
                  onClick={() => setNumClusters(Math.min(8, numClusters + 1))}
                  className="p-2 bg-gray-200 rounded-lg hover:bg-gray-300 disabled:opacity-50"
                  disabled={isRunning || numClusters >= 8}
                >
                  <Plus className="w-5 h-5" />
                </button>
                <span className="ml-2">Número de Grupos</span>
              </div>

              <button
                onClick={() => runKMeans()}
                className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                disabled={isRunning || points.length < numClusters}
              >
                <RefreshCw className={`w-5 h-5 ${isRunning ? 'animate-spin' : ''}`} />
                {isRunning ? 'Processando...' : 'Agrupar Pontos'}
              </button>
            </div>

            <div className="flex flex-col md:flex-row items-center gap-4 mt-6">
              <label className="flex items-center gap-2">
                <span className="text-sm text-gray-700">Limiar de dispersão:</span>
                <input
                  type="range"
                  min={50}
                  max={300}
                  value={dispersionThreshold}
                  onChange={e => setDispersionThreshold(Number(e.target.value))}
                  className="w-40 accent-pink-500"
                />
                <span className="text-pink-600 font-bold">{dispersionThreshold}px</span>
              </label>
              <span className="text-xs text-gray-500">Ajuste para controlar quando um novo cluster será criado automaticamente.</span>
            </div>
            <div className="flex flex-col md:flex-row items-center gap-4 mt-6">
              <label className="flex items-center gap-2">
                <span className="text-sm text-gray-700">Valor categórico (opcional):</span>
                <input
                  type="text"
                  value={categoricalValue}
                  onChange={e => setCategoricalValue(e.target.value)}
                  placeholder="Ex: Azul, Cliente A, etc."
                  className="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-green-300"
                  maxLength={20}
                />
                <button
                  onClick={handleAddCategoricalPoint}
                  className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
                >Adicionar</button>
              </label>
              {lastNumericValue !== null && (
                <span className="text-xs text-green-700">Último valor convertido: <b>{lastNumericValue}</b></span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;