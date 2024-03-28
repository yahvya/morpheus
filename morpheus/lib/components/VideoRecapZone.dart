import 'package:flutter/cupertino.dart';
import 'package:morpheus/config/ThemeConfig.dart';
import 'package:video_player/video_player.dart';

/// zone de recapitulatif de vidéo
class VideoRecapZone extends StatelessWidget{
  const VideoRecapZone({super.key,required this.name,required this.videoPath, this.width=140, this.height=140});

  final String name;
  final String videoPath;
  final double width;
  final double height;

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
          width: width,
          height: height,
          child: VideoPlayer(videoController),
        ),
        const SizedBox(height: 15,),
        Text(name, style: TextStyle(color: ThemeConfig.backgroundTextColor))
      ],
    );
  }
}
