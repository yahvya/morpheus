import 'package:flutter/cupertino.dart';
import 'package:video_player/video_player.dart';

/// zone de recapitulatif de vidéo
class VideoRecapZone extends StatelessWidget{
  const VideoRecapZone({super.key,required this.name,required this.videoPath});

  final String name;
  final String videoPath;

  @override
  Widget build(BuildContext context){
    var videoController = VideoPlayerController.asset(videoPath);

    videoController.initialize();
    videoController.setLooping(true);
    videoController.setVolume(100.0);
      videoController.play();

    return Column(
      children: [
        Container(
          width: 140,
          height: 140,
          child: VideoPlayer(videoController),
        ),
        const SizedBox(height: 15,),
        Text(name)
      ],
    );
  }
}
