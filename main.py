#!/usr/bin/env python3
"""
a script that removes the software imposed CPS limit of the Superstrike X3
before: a minimum of 50ms between clicks, making drag clicking not worth it
after: a minimum of ~10ms

requires hidapi 0.15.0 or newer: python -m pip install "hidapi>=0.15.0"

!! this has only been tested on firmware version 'AM 1.2.0015' for the Superstrike X3
!! it's also 101% not going to work on any other combination without targetted changes.

since the patch only lives in RAM, doing a cold reboot of the mouse will
drop these changes. on the upside, this also means that any permanent damage
is very unlikely to happen due to these changes.

----------------

the mouse has its own firmware updater, and that updater has an integer overflow
in the type-2 record parser's 32-bit offset + length calculation. normally that
parser only accepts a relative write inside its intended RAM object, but with the
overflow, both the bounds-check sum and the destination address wrap around, so
we can write to RAM anywhere (albeit sequentially) and point the record at the TCM 
where the active mouse handling is running.

since we only get one continuous write we put a wrapper over the beginning
of the HITS host-command handler at 0x22005b2c, copy the original bytes between
that address and the live sensor callback, and install the callback hook at
0x22005ea4 in the final packet.

----------------

the changes are:

1. point quiver at the config where all the timing values are 0 to get rid
   of the ~50ms quiver timing cycle
2. clear the 2 flags that make HITS ignore the sensor for 10ms after the haptic
   driver changes state (which apparently happens even when haptics are off).

with these patches, both software imposed delays are removed.
"""

import time

PACKET_TEMPLATE = tuple(
    bytes.fromhex(packet) if packet is not None else None
    for packet in (
        # packet 1: declare RDFU block and its total size of 0x2050 bytes.
        "06000100002050000000000000000000",
        
        # packet 2-3: we start with a type 1 packet that does nothing. the software
        # requires one type 1 packet before sending a type 2 packet,
        # which is what actually changes RAM
        None,
        "00000000000000000000000000000000",
        
        # packet 4: the type 2 record that triggers the overflow. normally it adds an offset to
        # 0x2f005684, but since it wraps around, we can give send an offset that ends up at
        # 0x22005b2c. that is where we start writing
        "02f30004a80cfffb5900000000000000",

        # packets 5-8: this is the whole wrapper
        #     ldr r3, =0x22005ea9      # return address when the sensor callback called us
        #     cmp lr, r3
        #     bne hits_command         # a different return address means setConfig called us
        #
        # sensor_callback:
        #     ldr r2, =0x2f003e3c      # where live Quiver keeps its config pointer
        #     ldr r3, =slot_config     # zero timing table in the active slot
        #     str r3, [r2]
        #     ldr r2, =0x2f005654      # the 2 flags that cause the 10ms ignores
        #     movs r3, #0
        #     strh r3, [r2]            # clear both at once before every HITS run
        #     ldr r3, =0x22005ec1      # logitech's original handler (see packet 60)
        #                              # has +1 because we run as Thumb code
        #     bx r3                    # jump into it and let it return normally
        #
        # hits_command:
        # RDFU cleanup path
        #     ldr r0, =0x2f004e10      # reset takes the live RDFU object as argument 1
        #     ldr r3, =slot_reset + 1  # active slot's reset address in Thumb mode
        #     bx r3                    # reset RDFU and let it return through existing lr
        "064b9e4507d1064a064b1360064a0023",
        "1380064b18470648064b1847a95e0022",
        None,
        None,

        # packets 9-59: unrelated bytes. since we can't jump over this area
        # we have to write through it. these are the original bytes here
        # so nothing changes
        "01f011f902a90522304602958df80c50",
        "01f04af99df808309df80910644a6548",
        "d1549df80a10644ad1549df80b10634a",
        "d1549df80c206249ca54182101fb0300",
        "60490069c95cfbf7c5fb204604b0bde8",
        "704000f059bd01f05bf8037842680290",
        "03f5807352f82350002dfbd102a801f0",
        "daf802a904223046029501f015f99df8",
        "08009df80b309df809109df80a2084f8",
        "3e00606984f83f1084f8402084f84130",
        "03689b689847c4e90a006062204604b0",
        "bde8704000f014bc01f02af803784268",
        "029003f5807352f82350002dfbd102a8",
        "01f0a9f802a902223046adf8085001f0",
        "e3f89df80930bdf80820b3fa83f36069",
        "5b09a4f8442084f8433003689b689847",
        "20634ff6ff70304b304c3149314a1d80",
        "5d80314b258008801560658048805560",
        "1d8004b070bd00f0f3ff037842680290",
        "03f5807352f82350002dfbd102a801f0",
        "72f80622304602a90295adf80c5001f0",
        "abf89df80850012de3d81822154b02fb",
        "05331e69174b595d9df80d30d3b1144b",
        "30465a5dfbf72efb9df80c3013b13046",
        "fbf708fb9df80a20144b60695a559df8",
        "0b20134b5a5503689b689847114b43f8",
        "2500bee730469df80920fbf7fffae3e7",
        None,
        "e60c002f6656002f4254002f4654002f",
        "d60c002f9046002f4054002f5856002f",
        "5656002f8846002f042970b504460dd8",
        "51b3037e43bb006901f0e0fc2046fff7",
        "dffd2046fff7ccfe01231ce008291bd1",
        "037ecbb1fff7fcfd0c4e0d4d002142f2",
        "107001f04bfdfff793fc327829780948",
        "fbf7d0fa727869780748fbf7cbfa2069",
        "01f0b8fc0023237670bd00bfe60c002f",
        None,
        "d3e8ef1f002904d1c3e8ec2fbcf1000f",
        "f6d190f83c3013b1006901f00bbd7047",
        "3446002f10b590f83c30002b29d04ff4",
        "0072154b00245b6859688a6459688a60",
        "59684a644ff4807259688a6459688a60",
        "08215b685a640d4b5b685a6891640421",
        "5a68c2f88c405a6891645b680121c3f8",
        "8840006901f0aafc0548fdf7bdf82046",
        None,
        None,
        "c36903bb0b79022b20d190f848302bb1",
        "0b6808469b689847002038bd0846faf7",
        "dbf8606903689b68984794f842300146",

        # packet 60: this memory zone is part of HITS button handling and is
        #  what runs and jumps to the earlier wrapper (packet 5-6, 0x22005b2c)
        # in logitech's original code, the instruction at 0x22005ea4 is `bl 0x22005ec0`
        # which calls the original HITS handler. bytes 8-11 of this packet replace only
        # that instruction with `bl 0x22005b2c` to jump to our wrapper
        "e06123b929462046fff742feece72046",
    )
)


SLOT_SPECIFIC_PACKET_NUMBERS = (2, 7, 8, 36, 46, 55, 56)

ENTITY_4_ACTIVE_PACKETS = tuple(
    bytes.fromhex(packet)
    for packet in (
        "010e041ff00000001000000000000000",  # packet 2: type-1 record for inactive entity 3
        "3c3e002f58d70b0e5456002fc15e0022",  # packet 7: entity 4 Quiver cfg pointer
        "104e002f7d500b0e2350002dfbd102a8",  # packet 8: entity 4 RDFU reset pointer
        "ea0c002f90be0b0ee80c002f5c56002f",  # packet 36: preserved entity-4 flash pointers
        "6656002fc89c0b0ea49c0b0e0122084b",  # packet 46: preserved entity-4 flash pointers
        "10bd6ff00400fbe7d4990b0eb0990b0e",  # packet 55: preserved entity-4 flash pointers
        "809c0b0e38b590f83c3004460d4613b3",  # packet 56: preserved entity-4 flash pointers
    )
)

ENTITY_3_ACTIVE_PACKETS = tuple(
    bytes.fromhex(packet)
    for packet in (
        "010e093ff00000001000000000000000",  # packet 2: type-1 record for inactive entity 4
        "3c3e002f38b7060e5456002fc15e0022",  # packet 7: entity 3 Quiver cfg pointer
        "104e002f6d30060e2350002dfbd102a8",  # packet 8: entity 3 RDFU reset pointer
        "ea0c002f709e060ee80c002f5c56002f",  # packet 36: preserved entity-3 flash pointers
        "6656002fb07c060e8c7c060e0122084b",  # packet 46: preserved entity-3 flash pointers
        "10bd6ff00400fbe7bc79060e9879060e",  # packet 55: preserved entity-3 flash pointers
        "687c060e38b590f83c3004460d4613b3",  # packet 56: preserved entity-3 flash pointers
    )
)
LOGITECH_VENDOR_ID = 0x046D
ANY_PRODUCT_ID = 0x0000
SUPERSTRIKE_RECEIVER_PRODUCT_IDS = (0xC54D, 0xC54F, 0xAB24)
HIDPP_USAGE_PAGES = (0xFF00, 0xFF43)
HID_DESCRIPTOR_REPORT_ID_TAG = 0x85
EXPECTED_HIDPP_INTERFACE_COUNT = 1

HIDPP_SHORT_REPORT_ID = 0x10
HIDPP_LONG_REPORT_ID = 0x11
HIDPP_VERY_LONG_REPORT_ID = 0x12
HIDPP_REPLY_REPORT_IDS = (
    HIDPP_SHORT_REPORT_ID,
    HIDPP_LONG_REPORT_ID,
    HIDPP_VERY_LONG_REPORT_ID,
)
HIDPP_SHORT_REPORT_LENGTH = 7
HIDPP_LONG_REPORT_LENGTH = 20
HIDPP_VERY_LONG_REPORT_LENGTH = 64
HIDPP_MAX_REPORT_LENGTH = HIDPP_VERY_LONG_REPORT_LENGTH
HIDPP_HEADER_LENGTH = 4
HIDPP_REPORT_ID_BYTE = 0
HIDPP_DEVICE_INDEX_BYTE = 1
HIDPP_FEATURE_INDEX_BYTE = 2
HIDPP_FUNCTION_BYTE = 3
HIDPP_PARAMETERS_BYTE = 4
HIDPP_PARAMETERS = slice(HIDPP_PARAMETERS_BYTE, None)
HIDPP_FUNCTION_SHIFT = 4
HIDPP_FUNCTION_MASK = 0xF0
HIDPP_PADDING_BYTE = b"\0"
PROTOCOL_BYTE_ORDER = "big"

HIDPP_ERROR_MARKER = 0xFF
HIDPP_ERROR_MARKER_BYTE = 2
HIDPP_ERROR_FEATURE_BYTE = 3
HIDPP_ERROR_FUNCTION_BYTE = 4
HIDPP_ERROR_CODE_BYTE = 5
HIDPP_ERROR_REPORT_LENGTH = 6

RECEIVER_DEVICE_INDEX = 1
BROADCAST_DEVICE_INDEX = 0xFF
VALID_REPLY_DEVICE_INDEXES = (RECEIVER_DEVICE_INDEX, BROADCAST_DEVICE_INDEX)

HOST_SOFTWARE_ID = 0x0E
RDFU_SOFTWARE_ID = 0x00
REQUEST_TIMEOUT_SECONDS = 0.75
DRAIN_READ_TIMEOUT_MS = 1
MILLISECONDS_PER_SECOND = 1000

ROOT_FEATURE_INDEX = 0x00
FEATURE_FIRMWARE_INFO = 0x0003
FEATURE_RDFU = 0x00D1
FEATURE_HITS = 0x1B0C
FEATURE_ID_LENGTH = 2

ROOT_GET_FEATURE = 0
FIRMWARE_GET_ENTITY_COUNT = 0
FIRMWARE_GET_ENTITY_INFO = 1
RDFU_START_DFU = 1
RDFU_GET_STATUS = 2
RDFU_TRANSFER_DATA = 4
HITS_SET_CONFIG = 1
HITS_GET_CONFIG = 2
HITS_GET_MONITORING = 4

APPLICATION_ENTITIES = (3, 4)
APPLICATION_ENTITY_TYPE = 15
APPLICATION_PREFIX = b"AM"
ACTIVE_VERSION_BYTES = bytes.fromhex("01020015")
ENTITY_TYPE_BYTE = 0
ENTITY_PREFIX = slice(1, 3)
ENTITY_VERSION = slice(4, 8)
ENTITY_FLAGS_BYTE = 8
ENTITY_ACTIVE_FLAG = 1
FIRMWARE_ENTITY_COUNT_BYTE = HIDPP_PARAMETERS_BYTE
FIRMWARE_ENTITY_BODY = HIDPP_PARAMETERS

RDFU_DFU_NOT_STARTED = 1
RDFU_DATA_TRANSFER_READY = 2
RDFU_PACKET_ACK = 6
RDFU_INITIAL_BLOCK = 0
RDFU_EXPECTED_BLOCK = 1
RDFU_START_MAGIC = bytes.fromhex("414d315f443100000000")
RDFU_BLOCK_ZERO_HEADER = bytes.fromhex("06000000000000100000000000000000")
RDFU_REPLY_ENTITY_BYTE = 4
RDFU_REPLY_STATUS_BYTE = 5
RDFU_REPLY_PARAMETERS_BYTE = 6
RDFU_BLOCK_LENGTH = 2
RDFU_ACK_LENGTH = 4
RDFU_REPLY_BLOCK = slice(
    RDFU_REPLY_PARAMETERS_BYTE,
    RDFU_REPLY_PARAMETERS_BYTE + RDFU_BLOCK_LENGTH,
)
RDFU_REPLY_ACK = slice(
    RDFU_REPLY_PARAMETERS_BYTE,
    RDFU_REPLY_PARAMETERS_BYTE + RDFU_ACK_LENGTH,
)

HITS_LEFT_BUTTON = 0
HITS_RIGHT_BUTTON = 1
HITS_BUTTONS = (HITS_LEFT_BUTTON, HITS_RIGHT_BUTTON)
HITS_ACTUATION_1_RAW = 4
HITS_RAPID_TRIGGER_1_ON_RAW = 5
HITS_HAPTICS_1_RAW = 4
HITS_CONFIG_LENGTH = 4
HITS_CONFIG_REPLY = slice(
    HIDPP_PARAMETERS_BYTE,
    HIDPP_PARAMETERS_BYTE + HITS_CONFIG_LENGTH,
)
HITS_MONITORING_FLAGS_BYTE = HIDPP_PARAMETERS_BYTE
HITS_MONITORING_MASK = 0x03

PATCH_PACKET_COUNT = 60
RDFU_PACKET_LENGTH = 16
FIRST_PACKET_NUMBER = 1


def build_packets(active_entity):
    slot_packets = {
        3: ENTITY_3_ACTIVE_PACKETS,
        4: ENTITY_4_ACTIVE_PACKETS,
    }[active_entity]

    packets = list(PACKET_TEMPLATE)
    for number, packet in zip(SLOT_SPECIFIC_PACKET_NUMBERS, slot_packets):
        packets[number - FIRST_PACKET_NUMBER] = packet
    return tuple(packets)


for active_entity in APPLICATION_ENTITIES:
    packets = build_packets(active_entity)
    assert len(packets) == PATCH_PACKET_COUNT
    assert all(len(packet) == RDFU_PACKET_LENGTH for packet in packets)
assert len(RDFU_BLOCK_ZERO_HEADER) == RDFU_PACKET_LENGTH


def open_receiver():
    try:
        import hid
    except ImportError as error:
        raise RuntimeError(
            "hidapi 0.15.0 or newer is required: "
            'python -m pip install "hidapi>=0.15.0"'
        ) from error

    candidates_by_path = {}
    seen = []
    open_errors = []
    report_id_item = bytes((HID_DESCRIPTOR_REPORT_ID_TAG, HIDPP_LONG_REPORT_ID))
    for info in hid.enumerate(LOGITECH_VENDOR_ID, ANY_PRODUCT_ID):
        product_id = int(info.get("product_id") or 0)
        seen.append(
            {
                "product_id": f"{product_id:04x}",
                "usage_page": f"{int(info.get('usage_page') or 0):04x}",
                "usage": f"{int(info.get('usage') or 0):04x}",
                "interface_number": info.get("interface_number"),
                "product_string": info.get("product_string"),
            }
        )
        if product_id not in SUPERSTRIKE_RECEIVER_PRODUCT_IDS:
            continue
        usage_page = int(info.get("usage_page") or 0)
        if usage_page != 0 and usage_page not in HIDPP_USAGE_PAGES:
            continue
        device = hid.device()
        try:
            device.open_path(info["path"])
            descriptor = bytes(device.get_report_descriptor())
            if report_id_item in descriptor:
                candidates_by_path[info["path"]] = info
        except OSError as error:
            open_errors.append(str(error))
        finally:
            device.close()

    candidates = list(candidates_by_path.values())
    if len(candidates) != EXPECTED_HIDPP_INTERFACE_COUNT:
        details = f" Logitech HID interfaces: {seen}."
        if open_errors:
            details += f" open errors: {open_errors}."
        raise RuntimeError(
            "expected one Superstrike receiver HID++ interface, "
            f"found {len(candidates)}.{details}"
        )

    device = hid.device()
    device.open_path(candidates[0]["path"])
    device.set_nonblocking(False)
    return device


def exchange(
    device,
    feature,
    function,
    params=b"",
    software=HOST_SOFTWARE_ID,
    match=True,
    drain=False,
):
    """send one HID++ request and wait for the reply"""
    if drain:
        while device.read(HIDPP_MAX_REPORT_LENGTH, DRAIN_READ_TIMEOUT_MS):
            pass

    function_nibble = function << HIDPP_FUNCTION_SHIFT
    request_header = bytes(
        (
            HIDPP_LONG_REPORT_ID,
            RECEIVER_DEVICE_INDEX,
            feature,
            function_nibble | software,
        )
    )
    request = (request_header + params).ljust(
        HIDPP_LONG_REPORT_LENGTH,
        HIDPP_PADDING_BYTE,
    )
    written = int(device.write(request))
    if written < len(request):
        raise RuntimeError(f"short HID++ write: {written}/{len(request)}")

    deadline = time.monotonic() + REQUEST_TIMEOUT_SECONDS
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"HID++ timeout: feature {feature:#x}, function {function}")
        timeout_ms = max(1, int(remaining * MILLISECONDS_PER_SECOND))
        reply = bytes(device.read(HIDPP_MAX_REPORT_LENGTH, timeout_ms))
        if not reply:
            raise TimeoutError(f"HID++ timeout: feature {feature:#x}, function {function}")

        # reject unrelated reports
        if (
            len(reply) < HIDPP_HEADER_LENGTH
            or reply[HIDPP_REPORT_ID_BYTE] not in HIDPP_REPLY_REPORT_IDS
            or reply[HIDPP_DEVICE_INDEX_BYTE] not in VALID_REPLY_DEVICE_INDEXES
        ):
            continue

        # raise any HID++ errors we get
        if (
            len(reply) >= HIDPP_ERROR_REPORT_LENGTH
            and reply[HIDPP_ERROR_MARKER_BYTE] == HIDPP_ERROR_MARKER
            and reply[HIDPP_ERROR_FEATURE_BYTE] == feature
            and (
                reply[HIDPP_ERROR_FUNCTION_BYTE] & HIDPP_FUNCTION_MASK
            ) == function_nibble
        ):
            error = reply[HIDPP_ERROR_CODE_BYTE]
            raise RuntimeError(f"HID++ error {error:#x}: {reply.hex()}")

        same_feature = reply[HIDPP_FEATURE_INDEX_BYTE] == feature
        same_function = (
            (reply[HIDPP_FUNCTION_BYTE] & HIDPP_FUNCTION_MASK)
            == function_nibble
        )
        if same_feature and (not match or same_function):
            return reply


def find_feature(device, feature_id):
    feature_bytes = feature_id.to_bytes(FEATURE_ID_LENGTH, PROTOCOL_BYTE_ORDER)
    reply = exchange(device, ROOT_FEATURE_INDEX, ROOT_GET_FEATURE, feature_bytes)
    if (
        len(reply) < HIDPP_SHORT_REPORT_LENGTH
        or not reply[HIDPP_PARAMETERS_BYTE]
    ):
        raise RuntimeError(f"feature {feature_id:#06x} unavailable")
    return reply[HIDPP_PARAMETERS_BYTE]


def main():
    device = open_receiver()
    sent = 0
    try:
        input("First move the mouse around to make sure it's awake, then leave it still and hit Enter.")
        firmware = find_feature(device, FEATURE_FIRMWARE_INFO)
        rdfu = find_feature(device, FEATURE_RDFU)
        hits = find_feature(device, FEATURE_HITS)

        # ensure that all conditions match, including 
        # the 1.2.0015 firmware, and that RDFU is parked
        count_reply = exchange(device, firmware, FIRMWARE_GET_ENTITY_COUNT)
        entity_count = count_reply[FIRMWARE_ENTITY_COUNT_BYTE]
        entries = [
            exchange(
                device,
                firmware,
                FIRMWARE_GET_ENTITY_INFO,
                bytes((entity,)),
            )[FIRMWARE_ENTITY_BODY]
            for entity in range(entity_count)
        ]
        active_entities = [
            entity
            for entity in APPLICATION_ENTITIES
            if entries[entity][ENTITY_FLAGS_BYTE] & ENTITY_ACTIVE_FLAG
        ]
        if len(active_entities) != 1:
            raise RuntimeError(f"expected only one active AM application entity, found {active_entities}")

        active_entity = active_entities[0]
        target_entity = 4 if active_entity == 3 else 3
        active = entries[active_entity]
        target = entries[target_entity]
        if not (
            active[ENTITY_TYPE_BYTE]
            == target[ENTITY_TYPE_BYTE]
            == APPLICATION_ENTITY_TYPE
            and active[ENTITY_PREFIX] == target[ENTITY_PREFIX] == APPLICATION_PREFIX
            and active[ENTITY_VERSION] == ACTIVE_VERSION_BYTES
            and active[ENTITY_FLAGS_BYTE] & ENTITY_ACTIVE_FLAG
            and not (target[ENTITY_FLAGS_BYTE] & ENTITY_ACTIVE_FLAG)
        ):
            raise RuntimeError("wrong firmware or slot layout. expected one active X3 AM 1.2.0015")

        packets = build_packets(active_entity)

        # make sure RDFU is stopped or waiting at block 0/1 for the inactive slot
        status = exchange(
            device,
            rdfu,
            RDFU_GET_STATUS,
            bytes((target_entity,)),
            software=RDFU_SOFTWARE_ID,
            match=False,
            drain=True,
        )
        status_entity = status[RDFU_REPLY_ENTITY_BYTE]
        status_code = status[RDFU_REPLY_STATUS_BYTE]
        status_block = int.from_bytes(
            status[RDFU_REPLY_BLOCK],
            PROTOCOL_BYTE_ORDER,
        )
        rdfu_not_started = (
            status_entity == target_entity
            and status_code == RDFU_DFU_NOT_STARTED
        )
        rdfu_ready_block_zero = (
            status_entity == target_entity
            and status_code == RDFU_DATA_TRANSFER_READY
            and status_block == RDFU_INITIAL_BLOCK
        )
        rdfu_ready_block_one = (
            status_entity == target_entity
            and status_code == RDFU_DATA_TRANSFER_READY
            and status_block == RDFU_EXPECTED_BLOCK
        )
        if not (rdfu_not_started or rdfu_ready_block_zero or rdfu_ready_block_one):
            raise RuntimeError(
                "RDFU is not stopped or waiting at block 0/1: "
                f"{status.hex()}"
            )

        # set 1/1/1 before patching and confirm it's set
        for button in HITS_BUTTONS:
            record = bytes(
                (
                    button,
                    HITS_ACTUATION_1_RAW,
                    HITS_RAPID_TRIGGER_1_ON_RAW,
                    HITS_HAPTICS_1_RAW,
                )
            )
            setter_reply = exchange(device, hits, HITS_SET_CONFIG, record)
            if setter_reply[HITS_CONFIG_REPLY] != record:
                raise RuntimeError("HITS 1/1/1 settings were not accepted")
            getter_reply = exchange(
                device,
                hits,
                HITS_GET_CONFIG,
                bytes((button,)),
            )
            if getter_reply[HITS_CONFIG_REPLY] != record:
                raise RuntimeError("HITS 1/1/1 settings were not applied")

        monitoring_reply = exchange(device, hits, HITS_GET_MONITORING)
        monitoring_flags = monitoring_reply[HITS_MONITORING_FLAGS_BYTE]
        if monitoring_flags & HITS_MONITORING_MASK:
            raise RuntimeError("disable HITS monitoring before patching (cold reboot)")

        if rdfu_not_started:
            start_reply = exchange(
                device,
                rdfu,
                RDFU_START_DFU,
                bytes((target_entity,)) + RDFU_START_MAGIC,
                software=RDFU_SOFTWARE_ID,
                match=False,
                drain=True,
            )
            start_entity = start_reply[RDFU_REPLY_ENTITY_BYTE]
            start_status = start_reply[RDFU_REPLY_STATUS_BYTE]
            start_block = int.from_bytes(
                start_reply[RDFU_REPLY_BLOCK],
                PROTOCOL_BYTE_ORDER,
            )
            if not (
                start_entity == target_entity
                and start_status == RDFU_DATA_TRANSFER_READY
                and start_block == RDFU_INITIAL_BLOCK
            ):
                raise RuntimeError(
                    f"RDFU did not start at block 0: {start_reply.hex()}"
                )
            rdfu_ready_block_zero = True

        if rdfu_ready_block_zero:
            block_zero_reply = exchange(
                device,
                rdfu,
                RDFU_TRANSFER_DATA,
                RDFU_BLOCK_ZERO_HEADER,
                software=RDFU_SOFTWARE_ID,
                match=False,
                drain=True,
            )
            block_zero_entity = block_zero_reply[RDFU_REPLY_ENTITY_BYTE]
            block_zero_status = block_zero_reply[RDFU_REPLY_STATUS_BYTE]
            next_block = int.from_bytes(
                block_zero_reply[RDFU_REPLY_BLOCK],
                PROTOCOL_BYTE_ORDER,
            )
            if not (
                block_zero_entity == target_entity
                and block_zero_status == RDFU_DATA_TRANSFER_READY
                and next_block == RDFU_EXPECTED_BLOCK
            ):
                raise RuntimeError(
                    "RDFU block-0 header did not advance to block 1: "
                    f"{block_zero_reply.hex()}"
                )

        for number, packet in enumerate(packets, FIRST_PACKET_NUMBER):
            reply = exchange(
                device,
                rdfu,
                RDFU_TRANSFER_DATA,
                packet,
                software=RDFU_SOFTWARE_ID,
                match=False,
                drain=number == FIRST_PACKET_NUMBER,
            )
            sent += 1
            reply_entity = reply[RDFU_REPLY_ENTITY_BYTE]
            reply_status = reply[RDFU_REPLY_STATUS_BYTE]
            reply_ack = int.from_bytes(reply[RDFU_REPLY_ACK], PROTOCOL_BYTE_ORDER)
            if not (
                reply_entity == target_entity
                and reply_status == RDFU_PACKET_ACK
                and reply_ack == number
            ):
                raise RuntimeError(f"bad RDFU ACK for packet {number}: {reply.hex()}")

        cleanup_trigger = bytes((HITS_LEFT_BUTTON, HITS_ACTUATION_1_RAW,
                                 HITS_RAPID_TRIGGER_1_ON_RAW, HITS_HAPTICS_1_RAW))
        try:
            exchange(device, hits, HITS_SET_CONFIG, cleanup_trigger)
        except (RuntimeError, TimeoutError):
            pass

        # setConfig returns immediately, so the HITS worker could still be running cleanup
        # we poll until it finishes or the normal req timeout expires
        cleanup_deadline = time.monotonic() + REQUEST_TIMEOUT_SECONDS
        expected_status = bytes((target_entity, RDFU_DFU_NOT_STARTED))
        while True:
            cleanup_status = exchange(
                device,
                rdfu,
                RDFU_GET_STATUS,
                bytes((target_entity,)),
                software=RDFU_SOFTWARE_ID,
                match=False,
            )
            if cleanup_status[RDFU_REPLY_ENTITY_BYTE:RDFU_REPLY_STATUS_BYTE + 1] == expected_status:
                break
            if time.monotonic() >= cleanup_deadline:
                raise RuntimeError(
                    "RDFU cleanup did not return the updater to not-started: "
                    f"{cleanup_status.hex()}"
                )
    except Exception:
        if sent:
            print("patch transmission has partially gone through, so cold reboot before retrying.")
        raise
    finally:
        device.close()

    print("Fast-click patch is active!")
    print("- do not change HITS while it's active.")
    print("- cold reboot to turn off.")


if __name__ == "__main__":
    main()
