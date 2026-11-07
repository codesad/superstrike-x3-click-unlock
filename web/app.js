const LOGITECH_VENDOR_ID = 0x046d;
const RECEIVER_PRODUCT_IDS = [0xc54d, 0xc54f, 0xab24];
const HIDPP_USAGE_PAGES = [0xff00, 0xff43];

const HIDPP_SHORT_REPORT_ID = 0x10;
const HIDPP_LONG_REPORT_ID = 0x11;
const HIDPP_VERY_LONG_REPORT_ID = 0x12;
const HIDPP_REPLY_REPORT_IDS = [
  HIDPP_SHORT_REPORT_ID,
  HIDPP_LONG_REPORT_ID,
  HIDPP_VERY_LONG_REPORT_ID,
];
const HIDPP_LONG_REPORT_LENGTH = 20;
const HIDPP_HEADER_LENGTH = 4;
const HIDPP_FUNCTION_SHIFT = 4;
const HIDPP_FUNCTION_MASK = 0xf0;
const HIDPP_ERROR_MARKER = 0xff;

const RECEIVER_DEVICE_INDEX = 1;
const BROADCAST_DEVICE_INDEX = 0xff;
const HOST_SOFTWARE_ID = 0x0e;
const RDFU_SOFTWARE_ID = 0x00;
const REQUEST_TIMEOUT_MS = 750;

const ROOT_FEATURE_INDEX = 0x00;
const ROOT_GET_FEATURE = 0;
const FEATURE_FIRMWARE_INFO = 0x0003;
const FEATURE_RDFU = 0x00d1;
const FEATURE_HITS = 0x1b0c;
const FIRMWARE_GET_ENTITY_COUNT = 0;
const FIRMWARE_GET_ENTITY_INFO = 1;
const RDFU_START_DFU = 1;
const RDFU_GET_STATUS = 2;
const RDFU_TRANSFER_DATA = 4;
const HITS_SET_CONFIG = 1;
const HITS_GET_CONFIG = 2;
const HITS_GET_MONITORING = 4;

const TARGET_APPLICATION_ENTITY = 3;
const ACTIVE_APPLICATION_ENTITY = 4;
const APPLICATION_ENTITY_TYPE = 15;
const APPLICATION_PREFIX = "AM";
const ACTIVE_VERSION_BYTES = [0x01, 0x02, 0x00, 0x15];

const RDFU_DFU_NOT_STARTED = 1;
const RDFU_DATA_TRANSFER_READY = 2;
const RDFU_PACKET_ACK = 6;
const RDFU_INITIAL_BLOCK = 0;
const RDFU_EXPECTED_BLOCK = 1;
const RDFU_START_MAGIC = hexToBytes("414d315f443100000000");
const RDFU_BLOCK_ZERO_HEADER = hexToBytes("06000000000000100000000000000000");

const HITS_BUTTONS = [0, 1];
const HITS_ACTUATION_1_RAW = 4;
const HITS_RAPID_TRIGGER_1_ON_RAW = 5;
const HITS_HAPTICS_1_RAW = 4;
const HITS_MONITORING_MASK = 0x03;

const PATCH_PACKET_HEX = [
  "06000100002050000000000000000000",
  "010e041ff00000001000000000000000",
  "00000000000000000000000000000000",
  "02f30004a80cfffb5900000000000000",
  "064b9e4507d1064a064b1360064a0023",
  "1380064b18470648064b1847a95e0022",
  "3c3e002f58d70b0e5456002fc15e0022",
  "104e002f7d500b0e2350002dfbd102a8",
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
  "ea0c002f90be0b0ee80c002f5c56002f",
  "e60c002f6656002f4254002f4654002f",
  "d60c002f9046002f4054002f5856002f",
  "5656002f8846002f042970b504460dd8",
  "51b3037e43bb006901f0e0fc2046fff7",
  "dffd2046fff7ccfe01231ce008291bd1",
  "037ecbb1fff7fcfd0c4e0d4d002142f2",
  "107001f04bfdfff793fc327829780948",
  "fbf7d0fa727869780748fbf7cbfa2069",
  "01f0b8fc0023237670bd00bfe60c002f",
  "6656002fc89c0b0ea49c0b0e0122084b",
  "d3e8ef1f002904d1c3e8ec2fbcf1000f",
  "f6d190f83c3013b1006901f00bbd7047",
  "3446002f10b590f83c30002b29d04ff4",
  "0072154b00245b6859688a6459688a60",
  "59684a644ff4807259688a6459688a60",
  "08215b685a640d4b5b685a6891640421",
  "5a68c2f88c405a6891645b680121c3f8",
  "8840006901f0aafc0548fdf7bdf82046",
  "10bd6ff00400fbe7d4990b0eb0990b0e",
  "809c0b0e38b590f83c3004460d4613b3",
  "c36903bb0b79022b20d190f848302bb1",
  "0b6808469b689847002038bd0846faf7",
  "dbf8606903689b68984794f842300146",
  "e06123b929462046fff742feece72046",
];

const PATCH_PACKETS = PATCH_PACKET_HEX.map(hexToBytes);

const actionButton = document.querySelector("#action");

let currentLink = null;
let stage = "connect";

class HidppLink {
  constructor(device) {
    this.device = device;
    this.pending = null;
    this.handleInputReport = this.handleInputReport.bind(this);
    this.device.addEventListener("inputreport", this.handleInputReport);
  }

  close() {
    this.device.removeEventListener("inputreport", this.handleInputReport);
    if (this.pending) {
      this.rejectPending(new Error("The receiver was disconnected."));
    }
    if (this.device.opened) {
      return this.device.close();
    }
    return Promise.resolve();
  }

  handleInputReport(event) {
    if (!this.pending || event.device !== this.device) {
      return;
    }

    const report = new Uint8Array(event.data.byteLength + 1);
    report[0] = event.reportId;
    report.set(
      new Uint8Array(event.data.buffer, event.data.byteOffset, event.data.byteLength),
      1,
    );

    if (
      report.length < HIDPP_HEADER_LENGTH ||
      !HIDPP_REPLY_REPORT_IDS.includes(report[0]) ||
      ![RECEIVER_DEVICE_INDEX, BROADCAST_DEVICE_INDEX].includes(report[1])
    ) {
      return;
    }

    const request = this.pending;
    const replyFunction = report[3] & HIDPP_FUNCTION_MASK;
    if (
      report.length >= 6 &&
      report[2] === HIDPP_ERROR_MARKER &&
      report[3] === request.feature &&
      (report[4] & HIDPP_FUNCTION_MASK) === request.functionNibble
    ) {
      this.rejectPending(
        new Error(`HID++ error 0x${hex(report[5], 2)}: ${bytesToHex(report)}`),
      );
      return;
    }

    const sameFeature = report[2] === request.feature;
    const sameFunction = replyFunction === request.functionNibble;
    if (sameFeature && (!request.matchFunction || sameFunction)) {
      this.resolvePending(report);
    }
  }

  resolvePending(report) {
    const request = this.pending;
    this.pending = null;
    clearTimeout(request.timeout);
    request.resolve(report);
  }

  rejectPending(error) {
    const request = this.pending;
    this.pending = null;
    clearTimeout(request.timeout);
    request.reject(error);
  }

  async exchange(
    feature,
    command,
    parameters = new Uint8Array(),
    software = HOST_SOFTWARE_ID,
    matchFunction = true,
  ) {
    if (this.pending) {
      throw new Error("Another HID++ request is still waiting for a reply.");
    }
    if (parameters.length > HIDPP_LONG_REPORT_LENGTH - HIDPP_HEADER_LENGTH) {
      throw new Error("HID++ parameters do not fit in a long report.");
    }

    const functionNibble = command << HIDPP_FUNCTION_SHIFT;
    const report = new Uint8Array(HIDPP_LONG_REPORT_LENGTH - 1);
    report[0] = RECEIVER_DEVICE_INDEX;
    report[1] = feature;
    report[2] = functionNibble | software;
    report.set(parameters, 3);

    const reply = new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.rejectPending(
          new Error(
            `HID++ timeout: feature 0x${hex(feature, 2)}, function ${command}`,
          ),
        );
      }, REQUEST_TIMEOUT_MS);
      this.pending = {
        feature,
        functionNibble,
        matchFunction,
        resolve,
        reject,
        timeout,
      };
    });

    try {
      await this.device.sendReport(HIDPP_LONG_REPORT_ID, report);
    } catch (error) {
      this.rejectPending(error);
    }
    return reply;
  }
}

function hex(value, width = 4) {
  return Number(value).toString(16).padStart(width, "0");
}

function hexToBytes(value) {
  if (value.length % 2 !== 0) {
    throw new Error("Invalid hexadecimal string.");
  }
  return Uint8Array.from(
    value.match(/../g) ?? [],
    (byte) => Number.parseInt(byte, 16),
  );
}

function bytesToHex(bytes) {
  return [...bytes].map((value) => hex(value, 2)).join("");
}

function bytesEqual(bytes, expected) {
  return bytes.length === expected.length &&
    expected.every((value, index) => bytes[index] === value);
}

function featureBytes(featureId) {
  return new Uint8Array([featureId >> 8, featureId & 0xff]);
}

function concatBytes(...parts) {
  const joined = new Uint8Array(parts.reduce((length, part) => length + part.length, 0));
  let offset = 0;
  for (const part of parts) {
    joined.set(part, offset);
    offset += part.length;
  }
  return joined;
}

function reportIds(collection, kind) {
  return [...(collection[kind] ?? [])].map((report) => report.reportId);
}

function isHidppInterface(device) {
  return device.collections.some((collection) => {
    const usageMatches = HIDPP_USAGE_PAGES.includes(collection.usagePage);
    const hasLongInput = reportIds(collection, "inputReports").includes(
      HIDPP_LONG_REPORT_ID,
    );
    const hasLongOutput = reportIds(collection, "outputReports").includes(
      HIDPP_LONG_REPORT_ID,
    );
    return usageMatches && hasLongInput && hasLongOutput;
  });
}

function parseRdfuStatus(reply) {
  const entity = reply[4];
  const code = reply[5];
  const block = (reply[6] << 8) | reply[7];
  const recognized =
    entity === TARGET_APPLICATION_ENTITY &&
    (code === RDFU_DFU_NOT_STARTED ||
      (code === RDFU_DATA_TRANSFER_READY &&
        [RDFU_INITIAL_BLOCK, RDFU_EXPECTED_BLOCK].includes(block)));

  return { entity, code, block, recognized, raw: bytesToHex(reply) };
}

async function findFeature(link, featureId) {
  const reply = await link.exchange(
    ROOT_FEATURE_INDEX,
    ROOT_GET_FEATURE,
    featureBytes(featureId),
  );
  if (reply.length < 7 || reply[4] === 0) {
    throw new Error(`HID++ feature 0x${hex(featureId)} is unavailable.`);
  }
  return reply[4];
}

async function getRdfuStatus(link, rdfuFeature) {
  const reply = await link.exchange(
    rdfuFeature,
    RDFU_GET_STATUS,
    new Uint8Array([TARGET_APPLICATION_ENTITY]),
    RDFU_SOFTWARE_ID,
    false,
  );
  return parseRdfuStatus(reply);
}

async function readCompatibility(link) {
  const firmwareFeature = await findFeature(link, FEATURE_FIRMWARE_INFO);
  const rdfuFeature = await findFeature(link, FEATURE_RDFU);
  const hitsFeature = await findFeature(link, FEATURE_HITS);

  const countReply = await link.exchange(
    firmwareFeature,
    FIRMWARE_GET_ENTITY_COUNT,
  );
  const entityCount = countReply[4];
  if (entityCount < 5 || entityCount > 32) {
    throw new Error(`Unexpected firmware entity count: ${entityCount}.`);
  }

  const target = (await link.exchange(
    firmwareFeature,
    FIRMWARE_GET_ENTITY_INFO,
    new Uint8Array([TARGET_APPLICATION_ENTITY]),
  )).slice(4);
  const active = (await link.exchange(
    firmwareFeature,
    FIRMWARE_GET_ENTITY_INFO,
    new Uint8Array([ACTIVE_APPLICATION_ENTITY]),
  )).slice(4);
  const layoutMatches =
    active[0] === APPLICATION_ENTITY_TYPE &&
    target[0] === APPLICATION_ENTITY_TYPE &&
    String.fromCharCode(active[1], active[2]) === APPLICATION_PREFIX &&
    String.fromCharCode(target[1], target[2]) === APPLICATION_PREFIX &&
    bytesEqual(active.slice(4, 8), ACTIVE_VERSION_BYTES) &&
    Boolean(active[8] & 1) &&
    !Boolean(target[8] & 1);

  const rdfuState = await getRdfuStatus(link, rdfuFeature);
  return {
    compatible: layoutMatches && rdfuState.recognized,
    firmwareSupported: layoutMatches,
    featureIndexes: {
      rdfu: rdfuFeature,
      hits: hitsFeature,
    },
    rdfuState,
  };
}

function requireRdfuState(state, code, block, message) {
  if (
    state.entity !== TARGET_APPLICATION_ENTITY ||
    state.code !== code ||
    state.block !== block
  ) {
    throw new Error(`${message}: ${state.raw}`);
  }
}

async function applyFastClickPatch(link) {
  const preflight = await readCompatibility(link);
  if (!preflight.compatible) {
    throw new Error("The firmware or RDFU state changed and is no longer compatible.");
  }

  const { rdfu: rdfuFeature, hits: hitsFeature } = preflight.featureIndexes;
  for (const button of HITS_BUTTONS) {
    const record = new Uint8Array([
      button,
      HITS_ACTUATION_1_RAW,
      HITS_RAPID_TRIGGER_1_ON_RAW,
      HITS_HAPTICS_1_RAW,
    ]);
    const setterReply = await link.exchange(
      hitsFeature,
      HITS_SET_CONFIG,
      record,
    );
    if (!bytesEqual(setterReply.slice(4, 8), record)) {
      throw new Error("HITS 1/1/1 settings were not accepted.");
    }

    const getterReply = await link.exchange(
      hitsFeature,
      HITS_GET_CONFIG,
      new Uint8Array([button]),
    );
    if (!bytesEqual(getterReply.slice(4, 8), record)) {
      throw new Error("HITS 1/1/1 settings were not applied.");
    }
  }

  const monitoringReply = await link.exchange(
    hitsFeature,
    HITS_GET_MONITORING,
  );
  if (monitoringReply[4] & HITS_MONITORING_MASK) {
    throw new Error("HITS monitoring is active. Cold reboot before patching.");
  }

  let rdfuState = preflight.rdfuState;
  if (rdfuState.code === RDFU_DFU_NOT_STARTED) {
    const startReply = await link.exchange(
      rdfuFeature,
      RDFU_START_DFU,
      concatBytes(new Uint8Array([TARGET_APPLICATION_ENTITY]), RDFU_START_MAGIC),
      RDFU_SOFTWARE_ID,
      false,
    );
    rdfuState = parseRdfuStatus(startReply);
    requireRdfuState(
      rdfuState,
      RDFU_DATA_TRANSFER_READY,
      RDFU_INITIAL_BLOCK,
      "RDFU did not start at block 0",
    );
  }

  if (
    rdfuState.code === RDFU_DATA_TRANSFER_READY &&
    rdfuState.block === RDFU_INITIAL_BLOCK
  ) {
    const blockZeroReply = await link.exchange(
      rdfuFeature,
      RDFU_TRANSFER_DATA,
      RDFU_BLOCK_ZERO_HEADER,
      RDFU_SOFTWARE_ID,
      false,
    );
    rdfuState = parseRdfuStatus(blockZeroReply);
    requireRdfuState(
      rdfuState,
      RDFU_DATA_TRANSFER_READY,
      RDFU_EXPECTED_BLOCK,
      "RDFU block 0 did not advance to block 1",
    );
  }

  requireRdfuState(
    rdfuState,
    RDFU_DATA_TRANSFER_READY,
    RDFU_EXPECTED_BLOCK,
    "RDFU is not ready for block 1",
  );

  for (let index = 0; index < PATCH_PACKETS.length; index += 1) {
    const number = index + 1;
    const reply = await link.exchange(
      rdfuFeature,
      RDFU_TRANSFER_DATA,
      PATCH_PACKETS[index],
      RDFU_SOFTWARE_ID,
      false,
    );
    const replyEntity = reply[4];
    const replyStatus = reply[5];
    const replyAck =
      (reply[6] * 0x1000000) +
      (reply[7] << 16) +
      (reply[8] << 8) +
      reply[9];
    if (
      replyEntity !== TARGET_APPLICATION_ENTITY ||
      replyStatus !== RDFU_PACKET_ACK ||
      replyAck !== number
    ) {
      throw new Error(`Bad RDFU ACK for packet ${number}: ${bytesToHex(reply)}`);
    }
  }

  const cleanupTrigger = new Uint8Array([
    HITS_BUTTONS[0],
    HITS_ACTUATION_1_RAW,
    HITS_RAPID_TRIGGER_1_ON_RAW,
    HITS_HAPTICS_1_RAW,
  ]);
  try {
    await link.exchange(hitsFeature, HITS_SET_CONFIG, cleanupTrigger);
  } catch {}

  const cleanupDeadline = Date.now() + REQUEST_TIMEOUT_MS;
  let cleanupState;
  while (true) {
    cleanupState = await getRdfuStatus(link, rdfuFeature);
    if (
      cleanupState.entity === TARGET_APPLICATION_ENTITY &&
      cleanupState.code === RDFU_DFU_NOT_STARTED
    ) {
      break;
    }
    if (Date.now() >= cleanupDeadline) {
      throw new Error(
        `RDFU cleanup did not return to not-started: ${cleanupState.raw}`,
      );
    }
  }
}

function setAction(label, disabled = false, state = "") {
  actionButton.textContent = label;
  actionButton.disabled = disabled;
  if (state) {
    actionButton.dataset.state = state;
  } else {
    delete actionButton.dataset.state;
  }
}

async function closeLink() {
  const link = currentLink;
  currentLink = null;
  if (!link) {
    return;
  }
  try {
    await link.close();
  } catch (error) {
    console.error(error);
  }
}

async function requestReceiver() {
  const filters = RECEIVER_PRODUCT_IDS.map((productId) => ({
    vendorId: LOGITECH_VENDOR_ID,
    productId,
  }));
  const devices = await navigator.hid.requestDevice({ filters });
  if (devices.length === 0) {
    throw new Error("No receiver was selected.");
  }

  const candidates = devices.filter(isHidppInterface);
  if (candidates.length === 0) {
    throw new Error("The selected receiver did not expose its HID++ interface.");
  }

  candidates.sort((left, right) => {
    const leftHasPreferredPage = left.collections.some(
      (collection) => collection.usagePage === 0xff43,
    );
    const rightHasPreferredPage = right.collections.some(
      (collection) => collection.usagePage === 0xff43,
    );
    return Number(rightHasPreferredPage) - Number(leftHasPreferredPage);
  });
  return candidates[0];
}

async function connect() {
  setAction("Select your receiver", true, "busy");

  try {
    await closeLink();

    const device = await requestReceiver();
    if (!device.opened) {
      await device.open();
    }
    currentLink = new HidppLink(device);

    setAction("Checking mouse...", true, "busy");
    const compatibility = await readCompatibility(currentLink);
    if (compatibility.compatible) {
      stage = "ready";
      setAction("Click to apply patch");
    } else {
      stage = "connect";
      await closeLink();
      setAction(
        compatibility.firmwareSupported
          ? "Unexpected mouse state. Reboot, then click to try again"
          : "Unsupported firmware. AM 1.2.0015 is required",
        false,
        "error",
      );
    }
  } catch (error) {
    console.error(error);
    stage = "connect";
    await closeLink();
    setAction("Click to try again", false, "error");
  }
}

async function applyPatch() {
  if (!currentLink) {
    stage = "connect";
    setAction("Click to connect mouse");
    return;
  }

  setAction("Applying patch...", true, "busy");
  try {
    await applyFastClickPatch(currentLink);
    setAction("Patch is active!", true, "success");
  } catch (error) {
    console.error(error);
    stage = "connect";
    setAction("Failed. Reboot, then click to try again", false, "error");
  } finally {
    await closeLink();
  }
}

async function primaryAction() {
  if (stage === "ready") {
    await applyPatch();
  } else if (stage === "connect") {
    await connect();
  }
}

if (!("hid" in navigator)) {
  setAction("WebHID is not supported in this browser", true, "error");
} else {
  actionButton.addEventListener("click", primaryAction);
}
