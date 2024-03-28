import 'package:flutter/material.dart';
import 'package:morpheus_team/style-config/app_theme.dart';

class AppCheckbox extends StatefulWidget {
  const AppCheckbox({super.key, required this.defaultCheckState,required this.onChanged});

  /// @brief Si la checkbox l'est par défaut
  final bool defaultCheckState;

  /// @brief Action au changement d'état de check
  final void Function(bool?) onChanged;

  @override
  AppCheckboxState createState() => AppCheckboxState();
}

class AppCheckboxState extends State<AppCheckbox> {
  late bool isChecked;

  @override
  void initState() {
    super.initState();
    isChecked = widget.defaultCheckState;
  }

  @override
  Widget build(BuildContext context) {
    return Checkbox(
      value: isChecked,
      onChanged: (newValue) {
        setState(() {
          isChecked = newValue!;
        });
        widget.onChanged(newValue);
      },
      activeColor: AppTheme.special,
      fillColor: MaterialStateProperty.all(AppTheme.special),
      checkColor: AppTheme.textOnSpecial,
      focusColor: AppTheme.special,
    );
  }
}
