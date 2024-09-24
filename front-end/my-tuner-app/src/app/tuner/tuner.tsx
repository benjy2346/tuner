'use client';
import { useEffect, useRef, useState } from 'react';

export default function Tuner() {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [feedback,setFeedback] = useState<string | null>(null);
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  useEffect(() => {
    // Create a WebSocket connection to the Flask back-end
    const ws = new WebSocket('ws://192.168.10.85:5000/audio-stream');
    setSocket(ws);

    // Cleanup WebSocket connection on component unmount
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const startPitchDetection = async () => {
    if (!socket) return;

    try {
      // Access the user's microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const audioCtx = new (window.AudioContext || window.AudioContext)();
      audioContextRef.current = audioCtx;

      const microphone = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 2048;

      microphone.connect(analyser);

      const bufferLength = analyser.fftSize;
      const dataArray = new Float32Array(bufferLength);

      const sendAudioData = () => {
        analyser.getFloatTimeDomainData(dataArray);
        
        // Send the audio data to the server over WebSocket
        if (socket && socket.readyState === WebSocket.OPEN) {
          socket.send(dataArray.buffer); // Send raw audio data
        }

        requestAnimationFrame(sendAudioData); // Continuously capture audio data
      };

      sendAudioData();
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Real-Time Pitch Tuner</h1>
      <p>{feedback ? feedback : 'Press the button to start detecting pitch.'}</p>
      <button onClick={startPitchDetection}>Start Pitch Detection</button>
    </div>
  );
}
