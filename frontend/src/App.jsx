import { useState, useRef, useEffect } from 'react';

function App() {
  const [syllabus, setSyllabus] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  const graphDataRef = useRef({ nodes: [], links: [] });

  useEffect(() => {
    // Start physics loop
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    // Resize handler
    const updateSize = () => {
        const parent = canvas.parentElement;
        if (parent) {
            canvas.width = parent.offsetWidth;
            canvas.height = parent.offsetHeight;
        }
    };
    window.addEventListener('resize', updateSize);
    updateSize(); // Initial resize

    // Physics Tunings
    const k = 0.05; 
    const repulsion = 4500; 
    const damping = 0.88; 
    const centerPull = 0.003;

    function animate() {
      const width = canvas.width;
      const height = canvas.height;
      
      // Draw background 
      ctx.fillStyle = '#0b1120';
      ctx.fillRect(0, 0, width, height);

      const { nodes, links } = graphDataRef.current;

      if (nodes.length > 0) {
          // 1. Repulsion
          for (let i = 0; i < nodes.length; i++) {
              for (let j = i + 1; j < nodes.length; j++) {
                  const dx = nodes[j].x - nodes[i].x;
                  const dy = nodes[j].y - nodes[i].y;
                  let distParams = dx * dx + dy * dy;
                  let dist = Math.sqrt(distParams) || 1;
                  
                  const force = repulsion / distParams;
                  const fx = (dx / dist) * force;
                  const fy = (dy / dist) * force;

                  nodes[i].vx -= fx;
                  nodes[i].vy -= fy;
                  nodes[j].vx += fx;
                  nodes[j].vy += fy;
              }
          }

          // 2. Spring
          links.forEach(link => {
              const dx = link.target.x - link.source.x;
              const dy = link.target.y - link.source.y;
              const dist = Math.sqrt(dx * dx + dy * dy) || 1;
              
              const targetDist = link.target.type === 'topic' ? 160 : 80;
              const force = (dist - targetDist) * k;
              const fx = (dx / dist) * force;
              const fy = (dy / dist) * force;

              link.source.vx += fx;
              link.source.vy += fy;
              link.target.vx -= fx;
              link.target.vy -= fy;
          });

          // 3. Motion
          nodes.forEach(node => {
              node.vx += (width / 2 - node.x) * centerPull;
              node.vy += (height / 2 - node.y) * centerPull;
              
              node.vx += (Math.random() - 0.5) * 0.4;
              node.vy += (Math.random() - 0.5) * 0.4;

              node.vx *= damping;
              node.vy *= damping;
              
              node.x += node.vx;
              node.y += node.vy;
          });

          // 4. Draw Links
          ctx.lineWidth = 1.2;
          links.forEach(link => {
              ctx.beginPath();
              ctx.moveTo(link.source.x, link.source.y);
              ctx.lineTo(link.target.x, link.target.y);
              
              const grad = ctx.createLinearGradient(link.source.x, link.source.y, link.target.x, link.target.y);
              grad.addColorStop(0, 'rgba(6, 182, 212, 0.4)'); 
              grad.addColorStop(1, 'rgba(168, 85, 247, 0.4)'); 
              ctx.strokeStyle = grad;
              ctx.stroke();
          });

          // 5. Draw Nodes
          nodes.forEach(node => {
              ctx.beginPath();
              let radius = 6;
              ctx.fillStyle = '#fff';
              ctx.shadowColor = 'transparent';
              ctx.shadowBlur = 0;

              if (node.type === 'root') {
                  radius = 14;
                  ctx.fillStyle = '#ffffff';
                  ctx.shadowColor = '#ffffff';
                  ctx.shadowBlur = 20;
              } else if (node.type === 'topic') {
                  radius = 10;
                  ctx.fillStyle = '#06b6d4';
                  ctx.shadowColor = '#06b6d4';
                  ctx.shadowBlur = 15;
              } else if (node.type === 'video') {
                  radius = 6;
                  ctx.fillStyle = '#a855f7';
                  ctx.shadowColor = '#a855f7';
                  ctx.shadowBlur = 10;
              }

              ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
              ctx.fill();

              // 6. Text Labels
              ctx.shadowBlur = 0;
              ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
              ctx.font = node.type === 'root' ? 'bold 13px sans-serif' : '11px sans-serif';
              ctx.textAlign = 'center';
              const textOffset = radius + 14;
              let label = node.label;
              if (label && label.length > 25) {
                  label = label.substring(0, 22) + '...';
              }
              ctx.fillText(label || "", node.x, node.y + textOffset);
          });
      }

      animationRef.current = requestAnimationFrame(animate);
    }

    animate();

    return () => {
        window.removeEventListener('resize', updateSize);
        if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, []);

  const updateGraph = (data) => {
      const nodes = [];
      const links = [];

      const canvas = canvasRef.current;
      const width = canvas ? canvas.width : 500;
      const height = canvas ? canvas.height : 500;

      nodes.push({ id: "Syllabus", type: "root", label: "Course", x: width/2, y: height/2, vx: 0, vy: 0 });

      const topics = Array.isArray(data) ? data : (data.course || []);

      topics.forEach((topic, i) => {
          nodes.push({ 
            id: topic.topic, 
            type: "topic", 
            label: topic.topic,
            x: width/2 + (Math.random()-0.5)*100,
            y: height/2 + (Math.random()-0.5)*100,
            vx: 0, vy: 0
           });
          links.push({ source: "Syllabus", target: topic.topic });

          if (topic.overview_video) {
              const vidId = topic.overview_video.video_id;
              nodes.push({
                  id: vidId,
                  type: "video",
                  label: topic.overview_video.title,
                  x: width/2 + (Math.random()-0.5)*200,
                  y: height/2 + (Math.random()-0.5)*200,
                  vx: 0, vy: 0
              });
              links.push({
                  source: topic.topic,
                  target: vidId
              });
          }
          
          if (topic.subtopics) {
            topic.subtopics.forEach((sub, j) => {
              if (sub.video) {
                  const subVidId = sub.video.video_id + "_" + j;
                  nodes.push({
                      id: subVidId,
                      type: "video",
                      label: sub.subtopic,
                      x: width/2 + (Math.random()-0.5)*300,
                      y: height/2 + (Math.random()-0.5)*300,
                      vx: 0, vy: 0
                  });
                  links.push({
                      source: topic.topic,
                      target: subVidId
                  });
              }
            });
          }
      });

      const nodeMap = new Map(nodes.map(n => [n.id, n]));
      links.forEach(l => {
          l.source = nodeMap.get(l.source);
          l.target = nodeMap.get(l.target);
      });

      graphDataRef.current = { nodes, links };
  };

  const generateCourse = async () => {
    if (!syllabus.trim()) return;

    setLoading(true);
    setResults([]);
    graphDataRef.current = { nodes: [], links: [] };

    try {
      const res = await fetch("http://127.0.0.1:8000/generate-course", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ syllabusText: syllabus })
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText || "Failed to generate course");
      }

      const data = await res.json();
      setResults(Array.isArray(data) ? data : (data.course || []));
      updateGraph(data);
    } catch (err) {
      console.error(err);
      setResults([{ error: err.message }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      generateCourse();
    }
  };
  
  const formatNumber = (num) => {
      if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
      if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
      return num;
  };

  return (
    <div style={{ display: 'flex', width: '100%', height: '100vh' }}>
      {/* Left Panel */}
      <div style={{ width: '50%', padding: '3rem 2.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', borderRight: '1px solid var(--border)', overflowY: 'auto' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '2.5rem', background: 'linear-gradient(to right, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Syllabus AI</h1>
          <p style={{ color: '#94a3b8', marginTop: '0.5rem', fontSize: '1.1rem' }}>Intelligent Parsing & Video Structuring</p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <textarea 
            value={syllabus}
            onChange={(e) => setSyllabus(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={`Paste your syllabus here...\nExample: GoBackN Protocol, SelectiveRepeat; TCP: Flow Control, Reno`}
            style={{ width: '100%', minHeight: '150px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '0.75rem', padding: '1.25rem', color: 'var(--text-color)', fontFamily: 'inherit', resize: 'vertical', fontSize: '1.05rem' }}
          />
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button 
              onClick={generateCourse}
              disabled={loading}
              style={{ background: loading ? 'var(--border)' : 'var(--primary)', color: 'white', border: 'none', padding: '0.85rem 1.75rem', borderRadius: '0.5rem', fontSize: '1.05rem', fontWeight: 'bold', cursor: loading ? 'not-allowed' : 'pointer', transition: 'background-color 0.2s' }}
            >
              {loading ? "Generating..." : "Generate Course"}
            </button>
            {loading && <div style={{ color: 'var(--cyan)', fontSize: '0.95rem', fontWeight: 500, animation: 'pulse 1.5s infinite' }}>Extracting AI Concepts...</div>}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', marginTop: '1rem' }}>
          {results.length === 0 && !loading && (
            <div style={{ color: '#94a3b8' }}>No topics structured from syllabus.</div>
          )}
          {results.map((topic, index) => {
            if (topic.error) {
              return <div key={index} style={{ color: '#ef4444', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px' }}>Error generating course: {topic.error}. Make sure the FastAPI backend is running!</div>
            }

            return (
              <div key={index} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '1rem', padding: '1.75rem', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
                <h2 style={{ color: 'var(--cyan)', margin: '0 0 1.25rem 0', fontSize: '1.4rem' }}>{topic.topic}</h2>

                <div style={{ fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', marginBottom: '0.75rem', fontWeight: 600 }}>Overview</div>
                {topic.overview_video ? (
                  <a href={`https://www.youtube.com/watch?v=${topic.overview_video.video_id}`} target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', background: 'rgba(0, 0, 0, 0.2)', padding: '0.85rem', borderRadius: '0.5rem', marginBottom: '1rem', textDecoration: 'none', color: 'inherit', border: '1px solid transparent', transition: 'background-color 0.2s', ':hover': {background: 'rgba(0,0,0,0.4)', borderColor: 'rgba(255,255,255,0.1)'} }}>
                    <img src={`https://img.youtube.com/vi/${topic.overview_video.video_id}/mqdefault.jpg`} alt="Thumbnail" style={{ width: '140px', height: '79px', borderRadius: '6px', objectFit: 'cover', background: '#1e293b' }} />
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                      <h3 style={{ fontWeight: 600, margin: 0, fontSize: '1rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>{topic.overview_video.title}</h3>
                      <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{topic.overview_video.channel} • {formatNumber(topic.overview_video.views || 0)} views</div>
                    </div>
                  </a>
                ) : (
                  <div style={{ color: '#ef4444', fontSize: '0.9rem' }}>No relevant video found.</div>
                )}

                {topic.subtopics && topic.subtopics.length > 0 && (
                  <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', marginBottom: '0.75rem', fontWeight: 600 }}>Detailed Subtopics</div>
                    {topic.subtopics.map((sub, j) => (
                      <div key={j} style={{ marginBottom: '1.25rem' }}>
                        <div style={{ fontSize: '1.05rem', color: 'var(--text-color)', marginBottom: '0.75rem', fontWeight: 500 }}>{sub.subtopic}</div>
                        {sub.video ? (
                          <a href={`https://www.youtube.com/watch?v=${sub.video.video_id}`} target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', background: 'rgba(168, 85, 247, 0.05)', padding: '0.85rem', borderRadius: '0.5rem', textDecoration: 'none', color: 'inherit', borderLeft: '2px solid transparent', transition: 'background-color 0.2s' }}>
                            <img src={`https://img.youtube.com/vi/${sub.video.video_id}/mqdefault.jpg`} alt="Thumbnail" style={{ width: '140px', height: '79px', borderRadius: '6px', objectFit: 'cover', background: '#1e293b' }} />
                            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                              <h3 style={{ fontWeight: 600, margin: 0, fontSize: '1rem', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>{sub.video.title}</h3>
                              <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{sub.video.channel} • {formatNumber(sub.video.views || 0)} views</div>
                            </div>
                          </a>
                        ) : (
                          <div style={{ color: '#ef4444', fontSize: '0.9rem' }}>No video found.</div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Right Panel */}
      <div style={{ width: '50%', position: 'relative', background: '#0b1120', overflow: 'hidden' }}>
        <canvas ref={canvasRef} style={{ width: '100%', height: '100%', display: 'block' }} />
      </div>
    </div>
  );
}

export default App;
