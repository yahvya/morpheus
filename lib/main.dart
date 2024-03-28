import 'package:flutter/material.dart';
import 'package:morpheus_team/app/auth/authenticator.dart';
import 'package:morpheus_team/pages/home.dart';
import 'package:morpheus_team/pages/login.dart';

void main() {
  runApp(MaterialApp(
    title: "Morpheus",
    locale: const Locale("fr"),
    home: Authenticator.isUserLogged() ? const Home() : const Login()
  ));
}