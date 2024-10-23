#include "config.h"
#include <epan/packet.h>
#define EXAMPLE_PORT 55555
static int proto_EXAMPLE = -1;
void
proto_register_EXAMPLE(void)
{
    proto_EXAMPLE = proto_register_protocol (
        "EXAMPLE Protocol",     /* name        */
        "EXAMPLE",              /* short name  */
        "EXAMPLE"               /* filter_name */
        );
}


void proto_reg_handoff_EXAMPLE(void)
{
    static dissector_handle_t EXAMPLE_handle;
    EXAMPLE_handle = create_dissector_handle(dissect_EXAMPLE, proto_EXAMPLE);
    dissector_add_uint("udp.port", EXAMPLE_PORT, EXAMPLE_handle);
}

static int dissect_EXAMPLE(tvbuff_t *etvb, packet_info *pinfo, proto_tree *tree _U_, void *data _U_)
{
    col_set_str(pinfo->cinfo, COL_PROTOCOL, "EXAMPLE");    
    col_clear(pinfo->cinfo,COL_INFO);
    return etvb_captured_length(etvb);
}