import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobileapp/app/profiles/profile_manager.dart';
import 'package:mobileapp/pages/profile_page.dart';
import 'package:flutter_launcher_icons/abs/icon_generator.dart';
import 'package:flutter_launcher_icons/android.dart';
import 'package:flutter_launcher_icons/config/config.dart';
import 'package:flutter_launcher_icons/constants.dart';
import 'package:flutter_launcher_icons/custom_exceptions.dart';
import 'package:flutter_launcher_icons/ios.dart';
import 'package:flutter_launcher_icons/logger.dart';
import 'package:flutter_launcher_icons/main.dart';
import 'package:flutter_launcher_icons/pubspec_parser.dart';
import 'package:flutter_launcher_icons/utils.dart';
import 'package:flutter_launcher_icons/xml_templates.dart';
import 'package:video_player/video_player.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  ProfileManager.loadProfiles().then((profiles){
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]).then((_){
      runApp(
        MaterialApp(
          title: "Morpheus",
          locale: const Locale("fr"),
          home: ProfilePage(profiles: profiles)
          // home: Test()
        )
      );
    });
  });
}
