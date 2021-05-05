
:main
  setlocal enabledelayedexpansion
  call :get-ini config.ini OPTIONS LANGUAGE result
  IF EXIST localisation\%result%.py (
    copy localisation\%result%.py bin\localisationdata.py >NUL
  ) ELSE (
    copy localisation\en.py bin\localisationdata.py >NUL
  )

  FOR /D %%G IN (lib/*) DO (
  
    IF NOT EXIST ./lib/%%G/controls.ini (
      copy lib\%%G\defaultControls.ini lib\%%G\controls.ini >NUL
    )

    IF NOT EXIST ./lib/%%G/pinout.ini (
      copy lib\%%G\defaultPinout.ini lib\%%G\pinout.ini >NUL
    )

    IF EXIST lib\%%G\localisation\%result%.py (
      copy lib\%%G\localisation\%result%.py lib\%%G\%%GLocalisationdata.py >NUL
    ) ELSE (
      copy lib\%%G\localisation\en.py lib\%%G\%%GLocalisationdata.py >NUL
    )
  )

  pip3 list | findstr pygments>nul || (
	pip3 install pygments
  )
  
  python ./bin/startMenu.py

  goto :eof


:get-ini <filename> <section> <key> <result>
  set %~4=
  setlocal
  set insection=
  for /f "usebackq eol=; tokens=*" %%a in ("%~1") do (
    set line=%%a
    if defined insection (
      for /f "tokens=1,* delims==" %%b in ("!line!") do (
        if /i "%%b"=="%3" (
          endlocal
          set %~4=%%c
          goto :eof
        )
      )
    )
    if "!line:~0,1!"=="[" (
      for /f "delims=[]" %%b in ("!line!") do (
        if /i "%%b"=="%2" (
          set insection=1
        ) else (
          endlocal
          if defined insection goto :eof
        )
      )
    )
  )
  endlocal
