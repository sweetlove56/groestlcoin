.PHONY: FORCE
all: FORCE
	$(MAKE) -C .. groestlcoin_qt test_groestlcoin_qt
clean: FORCE
	$(MAKE) -C .. groestlcoin_qt_clean test_groestlcoin_qt_clean
check: FORCE
	$(MAKE) -C .. test_groestlcoin_qt_check
groestlcoin-qt groestlcoin-qt.exe: FORCE
	 $(MAKE) -C .. groestlcoin_qt
apk: FORCE
	$(MAKE) -C .. groestlcoin_qt_apk
