import React, {useState, useRef} from 'react';

export default function Recorder({onTranscribed}){
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  async function start(){
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    const mr = new MediaRecorder(stream);
    mediaRecorderRef.current = mr;
    chunksRef.current = [];
    mr.ondataavailable = e => chunksRef.current.push(e.data);
    mr.onstop = async () => {
      const blob = new Blob(chunksRef.current, {type: 'audio/webm'});
      const fd = new FormData();
      fd.append('audio', blob, 'recording.webm');
      const res = await fetch('http://localhost:8000/transcribe', {method: 'POST', body: fd});
      const j = await res.json();
      onTranscribed && onTranscribed(j.text);
    }
    mr.start();
    setRecording(true);
  }

  function stop(){
    mediaRecorderRef.current.stop();
    setRecording(false);
  }

  return (
    <div>
      <button onClick={() => recording ? stop() : start()}>
        {recording ? 'Stop' : 'Record'}
      </button>
    </div>
  )
}
