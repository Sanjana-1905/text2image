import React, {useState} from 'react';
import Recorder from './components/Recorder';

export default function App(){
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState(null);

  async function onTranscribed(text){
    setPrompt(text);
  }

  async function generate(){
    const fd = new FormData();
    fd.append('prompt', prompt);
    const res = await fetch('http://localhost:8000/generate', {method: 'POST', body: fd});
    const j = await res.json();
    if (j.error) {
      alert('Error: ' + j.error);
      return;
    }
    setImageUrl('http://localhost:8000' + j.url);
  }

  return (
    <div style={{padding:20}}>
      <h1>Text/Voice → Image</h1>
      <Recorder onTranscribed={onTranscribed}/>
      <div>
        <textarea value={prompt} onChange={(e)=>setPrompt(e.target.value)} rows={4} cols={60}/>
      </div>
      <div>
        <button onClick={generate}>Generate Image</button>
      </div>
      {imageUrl && <div><h3>Result</h3><img src={imageUrl} style={{maxWidth:'512px'}} alt="generated"/></div>}
    </div>
  )
}
