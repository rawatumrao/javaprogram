// src/BitmovinPlayer.jsx
import React, { useEffect, useRef, useState } from 'react';
import { Player } from 'bitmovin-player';

const BitmovinPlayer = () => {
  const playerRef = useRef(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    // Initialize the player only once when the component mounts
    if (!player && videoUrl) {
      const newPlayer = new Player(playerRef.current, {
        key: 'YOUR_BITMOVIN_PLAYER_LICENSE_KEY', // Replace with your Bitmovin license key
        source: {
          dash: videoUrl, // You can use other formats like HLS, MP4, etc.
        },
      });
      setPlayer(newPlayer);
    }

    return () => {
      // Clean up the player instance when the component unmounts
      if (player) {
        player.destroy();
      }
    };
  }, [videoUrl, player]);

  const handleVideoChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const videoUrl = URL.createObjectURL(selectedFile);
      setVideoUrl(videoUrl);
    }
  };

  return (
    <div>
      <h1>Bitmovin Player</h1>
      <input
        type="file"
        accept="video/*"
        onChange={handleVideoChange}
      />
      <div
        ref={playerRef}
        style={{ width: '100%', height: '500px', background: 'black' }}
      ></div>
    </div>
  );
};

export default BitmovinPlayer;
