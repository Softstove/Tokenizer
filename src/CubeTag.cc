#include "onmt/CubeTag.h"

#include "onmt/Tokenizer.h"
#include "Utils.h"

namespace onmt
{

  // -------------------------------------------------------------------------
  // Constants
  // -------------------------------------------------------------------------

  // The placeholder content starts with this prefix so that the tokenizer can
  // distinguish CUBE tags from other arbitrary placeholders.
  const std::string CubeTagParser::tag_prefix = "cube";

  // -------------------------------------------------------------------------
  // CubeTag member functions
  // -------------------------------------------------------------------------

  bool CubeTag::valid() const
  {
    return !contact.empty() || !path.empty() || !regex.empty();
  }

  // -------------------------------------------------------------------------
  // CubeTagParser static helpers (internal)
  // -------------------------------------------------------------------------

  // Strips the surrounding ｟ … ｠ markers from a placeholder string and
  // returns the inner content, or an empty string if the input is not a
  // well-formed placeholder.
  static std::string strip_placeholder_markers(const std::string& placeholder)
  {
    const std::string& open  = Tokenizer::ph_marker_open;
    const std::string& close = Tokenizer::ph_marker_close;
    if (!starts_with(placeholder, open) || !ends_with(placeholder, close))
      return {};
    const size_t inner_start = open.size();
    const size_t inner_len   = placeholder.size() - open.size() - close.size();
    return placeholder.substr(inner_start, inner_len);
  }

  // -------------------------------------------------------------------------
  // CubeTagParser public interface
  // -------------------------------------------------------------------------

  bool CubeTagParser::is_cube_tag(const std::string& placeholder)
  {
    const std::string inner = strip_placeholder_markers(placeholder);
    // Content must start with "cube" followed by either ':' (has fields) or
    // end-of-string (bare tag with no fields).
    if (!starts_with(inner, tag_prefix))
      return false;
    if (inner.size() == tag_prefix.size())
      return true;  // bare ｟cube｠
    return inner[tag_prefix.size()] == ':';
  }

  CubeTag CubeTagParser::parse(const std::string& placeholder)
  {
    CubeTag tag;
    if (!is_cube_tag(placeholder))
      return tag;  // returns invalid tag

    const std::string inner = strip_placeholder_markers(placeholder);
    // The part after "cube:" contains semicolon-separated key=value pairs.
    const size_t fields_start = tag_prefix.size() + 1;  // skip "cube:"
    if (inner.size() < fields_start)
      return tag;  // bare ｟cube｠ with no fields

    const std::string fields_str = inner.substr(fields_start);
    const std::vector<std::string> fields = split_string(fields_str, ";");

    for (const std::string& field : fields)
    {
      const size_t eq = field.find('=');
      if (eq == std::string::npos)
        continue;
      const std::string key   = field.substr(0, eq);
      const std::string value = field.substr(eq + 1);
      if (key == "contact")
        tag.contact = value;
      else if (key == "path")
        tag.path = value;
      else if (key == "regex")
        tag.regex = value;
      else if (key == "corner")
        tag.corner = value;
    }

    return tag;
  }

  std::string CubeTagParser::encode(const CubeTag& tag)
  {
    std::string content = tag_prefix;
    std::string fields;

    auto add_field = [&](const std::string& key, const std::string& value) {
      if (value.empty())
        return;
      if (!fields.empty())
        fields += ";";
      fields += key + "=" + value;
    };

    add_field("contact", tag.contact);
    add_field("path",    tag.path);
    add_field("regex",   tag.regex);
    if (!tag.corner.empty() && tag.corner != cube_corner_bottom_front_left)
      add_field("corner", tag.corner);

    if (!fields.empty())
      content += ":" + fields;

    return Tokenizer::ph_marker_open + content + Tokenizer::ph_marker_close;
  }

  std::vector<CubeTag> CubeTagParser::find_corner_tags(const std::string& text)
  {
    std::vector<CubeTag> result;
    if (text.empty())
      return result;

    const std::string& open  = Tokenizer::ph_marker_open;
    const std::string& close = Tokenizer::ph_marker_close;

    size_t pos = 0;

    // Skip leading whitespace.
    while (pos < text.size() && std::isspace(static_cast<unsigned char>(text[pos])))
      ++pos;

    // Consume consecutive CUBE placeholders from the beginning of the text
    // (bottom-front-left corner of the player ID card).
    while (pos < text.size() && starts_with(text.substr(pos), open))
    {
      const size_t tag_start = pos;
      const size_t close_pos = text.find(close, tag_start + open.size());
      if (close_pos == std::string::npos)
        break;

      const size_t tag_end = close_pos + close.size();
      const std::string candidate = text.substr(tag_start, tag_end - tag_start);

      if (!is_cube_tag(candidate))
        break;

      result.push_back(parse(candidate));
      pos = tag_end;

      // Skip whitespace between consecutive tags.
      while (pos < text.size() && std::isspace(static_cast<unsigned char>(text[pos])))
        ++pos;
    }

    return result;
  }

}
