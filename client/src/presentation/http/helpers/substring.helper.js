function substring(value, start, end) {
  if (value == null) {
    return "";
  }

  const text = String(value);

  const startIndex = Number(start) || 0;
  const endIndex =
    end !== undefined && end !== null && end !== ""
      ? Number(end)
      : undefined;

  return text.substring(startIndex, endIndex);
}

module.exports = {
    substring,
};