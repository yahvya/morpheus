import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobileapp/app/profiles/profile_manager.dart';
import 'package:mobileapp/pages/profile_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  ProfileManager.loadProfiles().then((profiles){
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]).then((_){
      runApp(
        MaterialApp(
          title: "Morpheus",
          locale: const Locale("fr"),
          home: ProfilePage(profiles: profiles)
        )
      );
    });
  });
}