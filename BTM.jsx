import React, { useEffect, useRef, useState } from 'react';
import { Player } from 'bitmovin-player';

const BitmovinPlayer = () => {
  const playerRef = useRef(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    if (videoUrl && !player) {
      // Initialize the player when the video URL is available
      const newPlayer = new Player(playerRef.current, {
        key: 'YOUR_BITMOVIN_PLAYER_LICENSE_KEY', // Replace with your Bitmovin license key
        source: {
          mp4: videoUrl, // Set the mp4 URL as the source
        },
      });

      // Ensure the player is properly loaded
      newPlayer.on('ready', () => {
        console.log("Player is ready.");
        newPlayer.load().then(() => {
          newPlayer.play().then(() => {
            console.log("Video is playing");
          }).catch((error) => {
            console.error("Error trying to play the video:", error);
          });
        }).catch((error) => {
          console.error("Error loading video:", error);
        });
      });

      setPlayer(newPlayer);
    }

    // Cleanup player when component unmounts or videoUrl changes
    return () => {
      if (player) {
        player.destroy();
        setPlayer(null);
      }
    };
  }, [videoUrl, player]); // Trigger effect on videoUrl change

  const handleVideoChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Create a URL for the selected file and set it as the video source
      const videoUrl = URL.createObjectURL(selectedFile);
      setVideoUrl(videoUrl); // Set the videoUrl state to trigger player update
    }
  };

  return (
    <div>
      <h1>Bitmovin Player - MP4</h1>
      <input
        type="file"
        accept="video/mp4" // Ensure only MP4 files are accepted
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
