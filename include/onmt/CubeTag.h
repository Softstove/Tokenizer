#pragma once

#include <string>
#include <vector>

#include "onmt/opennmttokenizer_export.h"

namespace onmt
{

  // Corner position constants for CUBE tag placement on player ID cards.
  // The canonical position is bottom-front-left, matching the card layout spec.
  inline const std::string cube_corner_bottom_front_left = "bottom-front-left";

  // A CUBE tag embeds structured player-contact, routing-path, and regex-pattern
  // data inside a tokenizer placeholder.  The encoded form is the placeholder
  //   ｟cube:contact=<value>;path=<value>;regex=<value>｠
  // Any field may be omitted; only the fields that are non-empty are serialised.
  struct OPENNMTTOKENIZER_EXPORT CubeTag
  {
    std::string contact;  // Player contact / AI communication endpoint.
    std::string path;     // Routing path between player AIs.
    std::string regex;    // Pattern used for player discovery / message filtering.
    std::string corner;   // Positioning hint (default: bottom-front-left).

    CubeTag() : corner(cube_corner_bottom_front_left) {}

    // Returns true when the tag carries at least one piece of meaningful data.
    bool valid() const;

    bool operator==(const CubeTag& other) const
    {
      return contact == other.contact
          && path    == other.path
          && regex   == other.regex
          && corner  == other.corner;
    }
  };

  // Parses and encodes CubeTag values to/from the placeholder representation
  // used by the tokenizer (｟cube:...｠).
  class OPENNMTTOKENIZER_EXPORT CubeTagParser
  {
  public:
    // The prefix that identifies a CUBE placeholder inside ｟ … ｠.
    static const std::string tag_prefix;

    // Returns true when the string is a valid CUBE placeholder.
    static bool is_cube_tag(const std::string& placeholder);

    // Parses a CUBE placeholder string into a CubeTag.
    // Returns an empty (invalid) CubeTag if the string is not a CUBE placeholder.
    static CubeTag parse(const std::string& placeholder);

    // Encodes a CubeTag as a placeholder string suitable for embedding in text.
    static std::string encode(const CubeTag& tag);

    // Searches text for CUBE tags that are positioned at the corner
    // (beginning of the text), consistent with the bottom-front-left placement
    // on a player ID card.  Returns all consecutive leading CUBE placeholders.
    static std::vector<CubeTag> find_corner_tags(const std::string& text);
  };

}
