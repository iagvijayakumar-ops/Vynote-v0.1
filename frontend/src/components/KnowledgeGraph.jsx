import React, { useMemo } from 'react';
import ReactFlow, { MiniMap, Controls, Background } from 'reactflow';
import 'reactflow/dist/style.css';

const KnowledgeGraph = ({ notesText }) => {
  const { nodes, edges } = useMemo(() => {
    if (!notesText) return { nodes: [], edges: [] };

    const lines = notesText.split('\n');
    const newNodes = [];
    const newEdges = [];
    let titleNodeId = 'root';
    
    newNodes.push({
      id: titleNodeId,
      data: { label: 'LECTURE CORE' },
      position: { x: 300, y: 50 },
      style: { background: '#8b5cf6', color: 'white', fontWeight: 'bold', borderRadius: '12px', border: 'none', padding: '10px' }
    });

    let yOffset = 180;
    let xOffset = 50;
    
    lines.forEach((line, index) => {
      if (line.includes('Title:')) {
        newNodes[0].data.label = line.replace('📘 Title:', '').trim().toUpperCase();
      } 
      else if (line.trim().match(/^\d+\./)) {
         const pointLabel = line.substring(line.indexOf('.') + 1).split(':')[0]?.trim() || `Concept ${index}`;
         const nodeId = `node-${index}`;
         
         newNodes.push({
            id: nodeId,
            data: { label: pointLabel },
            position: { x: xOffset, y: yOffset },
            style: { background: 'rgba(255,255,255,0.05)', color: '#94a3b8', border: '1px solid rgba(139,92,246,0.2)', borderRadius: '12px', padding: '10px', fontSize: '12px' }
         });
         
         newEdges.push({
            id: `edge-${index}`,
            source: titleNodeId,
            target: nodeId,
            animated: true,
            style: { stroke: '#8b5cf6', opacity: 0.3 }
         });
         
         xOffset += 250;
         if (xOffset > 750) { xOffset = 50; yOffset += 120; }
      }
    });

    return { nodes: newNodes, edges: newEdges };
  }, [notesText]);

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden select-none">
       {!notesText ? (
          <div className="flex-1 flex items-center justify-center p-8 opacity-40 text-[10px] font-black uppercase tracking-widest text-slate-500">
             Knowledge projection pending...
          </div>
       ) : (
          <div className="flex-1 relative">
            <ReactFlow 
                nodes={nodes} 
                edges={edges} 
                fitView 
                className="bg-transparent"
            >
               <Background color="#1e1b4b" gap={20} size={1} />
               <Controls className="bg-slate-900 border-white/5 invert" />
               <MiniMap className="bg-slate-950/80 border-white/5" maskColor="rgba(0,0,0,0.5)" />
            </ReactFlow>
          </div>
       )}
    </div>
  );
};

export default KnowledgeGraph;
