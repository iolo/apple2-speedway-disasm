# Build only from editable ca65/BASIC source. The repaired hex/disk are used
# exclusively by the optional `verify` comparison target.
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:

CA65 ?= ca65
LD65 ?= ld65
A2KIT ?= a2kit
PYTHON ?= python3
BUILD := build

.PHONY: all disk binary verify clean
all: disk
disk: $(BUILD)/speedway.dsk
binary: $(BUILD)/speedway.bin $(BUILD)/loader.bin

$(BUILD):
	mkdir -p "$@"

$(BUILD)/speedway.o: src/speedway.s $(wildcard src/*.inc) | $(BUILD)
	$(CA65) -g -I src -l $(BUILD)/speedway.lst -o "$@" "$<"

$(BUILD)/speedway.bin: $(BUILD)/speedway.o src/speedway.cfg
	$(LD65) -C src/speedway.cfg -m $(BUILD)/speedway.map \
		-Ln $(BUILD)/speedway.lbl --dbgfile $(BUILD)/speedway.dbg -o "$@" "$<"

$(BUILD)/loader.o: src/loader.s | $(BUILD)
	$(CA65) -g -l $(BUILD)/loader.lst -o "$@" "$<"

$(BUILD)/loader.bin: $(BUILD)/loader.o src/loader.cfg
	$(LD65) -C src/loader.cfg -m $(BUILD)/loader.map \
		-Ln $(BUILD)/loader.lbl -o "$@" "$<"

$(BUILD)/speedway.dsk: $(BUILD)/speedway.bin $(BUILD)/loader.bin \
                     src/speedway-run.bas.in src/hello.bas tools/package_disk.py
	$(PYTHON) tools/package_disk.py --a2kit "$(A2KIT)" \
		--payload $(BUILD)/speedway.bin --loader $(BUILD)/loader.bin \
		--template src/speedway-run.bas.in --hello src/hello.bas --output "$@"

# Strict restoration check: intentional changes to code/assets may fail this.
verify: all
	$(PYTHON) tools/verify_build.py --build $(BUILD) \
		--hex "crowded speed way.hex" --basic speedway-run.bas --disk speedway.dsk

clean:
	rm -rf -- $(BUILD)
