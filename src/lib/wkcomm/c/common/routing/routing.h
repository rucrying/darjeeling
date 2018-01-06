#ifndef ROUTING_NONEH
#define ROUTING_NONEH

// ROUTING.H SHOULD BE THE SAME FOR ALL ROUTING LIBRARIES

#include "types.h"
#include "config.h"
#include "wkcomm.h"

extern void routing_init(void);

// This will be frequently called by Darjeeling to receive messages
// Shoudl return quickly if there's nothing to do
extern void routing_poll(void);

// This will be called from wkcomm when it needs to send a message
extern uint8_t routing_send(wkcomm_address_t dest, uint8_t *payload, uint8_t length);
extern uint8_t routing_send_raw(wkcomm_address_t dest, uint8_t *payload, uint8_t length);

#ifdef ROUTING_USE_GATEWAY
#define ROUTING_MPTN_OVERHEAD 9
extern void routing_discover_gateway(void);
#else
#define ROUTING_MPTN_OVERHEAD 0
#endif

// This will be called from wkcomm to determine this node's wukong id
wkcomm_address_t routing_get_node_id(void);
wkcomm_address_t routing_get_gateway_id(void);

// These will be called by the radios when it receives a message
#ifdef RADIO_USE_ZWAVE
#include "../radios/radio_zwave.h"
extern void routing_handle_zwave_message(radio_zwave_address_t zwave_addr, uint8_t *payload, uint8_t length);
#endif // RADIO_USE_ZWAVE

#ifdef RADIO_USE_XBEE
#include "../radios/radio_xbee.h"
extern void routing_handle_xbee_message(radio_xbee_address_t xbee_addr, uint8_t *payload, uint8_t length);
#endif // RADIO_USE_XBEE

#ifdef RADIO_USE_NETWORKSERVER
#include "../../posix/radios/radio_networkserver.h"
extern void routing_handle_local_message(radio_networkserver_address_t local_addr, uint8_t *payload, uint8_t length);
#endif // RADIO_USE_NETWORKSERVER

#ifdef RADIO_USE_WIFI
#include "../radios/radio_wifi.h"
extern void routing_handle_wifi_message(radio_wifi_address_t wifi_addr, uint8_t *payload, uint8_t length);
// extern void wifi_server_disconnect(uint8_t cid);
#endif // RADIO_USE_WIFI

#endif // ROUTING_NONEH

