
# TPClock — сборка и запуск (macOS)

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Запуск приложения в режиме разработки

```bash
python3 main.py
```

## 3. Сборка macOS .app

Способ 1 — через готовый spec:

```bash
pyinstaller main.spec
```

После сборки приложение появится в:

```
dist/TPClock.app
```

Способ 2 — ручная команда:

```bash
pyinstaller \
  --name TPClock \
  --windowed \
  --icon=icon.icns \
  --add-data "images_white:images_white" \
  --add-data "images_grey:images_grey" \
  --add-data "деления_и_цифры.svg:." \
  --add-data "hour_arrow.svg:." \
  --add-data "минутная_стрелка.svg:." \
  --add-data "секундная_стрелка.svg:." \
  main.py
```

## 4. Если macOS пишет «Приложение повреждено»

```bash
sudo xattr -rd com.apple.quarantine dist/TPClock.app
```

## 5. Готово!

Открой:

```
dist/TPClock.app
```

---
