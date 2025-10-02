// copied from 
// https://github.com/eclipse-threadx/netxduo/blob/master/samples/demo_mqtt_client.c
//
/**************************************************************************/
/*                                                                        */
/*       Copyright (c) Microsoft Corporation. All rights reserved.        */
/*                                                                        */
/*       This software is licensed under the Microsoft Software License   */
/*       Terms for Microsoft Azure RTOS. Full text of the license can be  */
/*       found in the LICENSE file at https://aka.ms/AzureRTOS_EULA       */
/*       and in the root directory of this software.                      */
/*                                                                        */
/**************************************************************************/

/* 

   This is a small demonstration of the high-performance NetX TCP/IP stack 
   MQTT client.

   This demo program establishes a connection to the Mosquitto server at IP address
   10.0.10.1.  It subscribes to a topic, send a message to the same topic.
   The application shall be able to receive the same message from the broker. 

   This demo assumes that the NetX Duo TCP/IP stack has been properly configured,
   with TCP module enabled.   The entry function is "thread_mqtt_entry".  Caller
   needs to pass in the IP instance and an instance of a valid packet pool. 
*/

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-variable"

#include "nx_api.h"
#include "nxd_mqtt_client.h"

#include "cloud_config.h"
#include "wwd_networking.h"
#include "board_init.h"


/* MQTT Demo defines */

/* IP Address of the local server. */
#define  LOCAL_SERVER_ADDRESS (IP_ADDRESS(MQTTSRVIP1, MQTTSRVIP2, MQTTSRVIP3, MQTTSRVIP4))


/*****************************************************************************************/
/* MQTT Local Server IoT Client example.                                                 */
/*****************************************************************************************/

#define  DEMO_STACK_SIZE            2048
#define  CLIENT_ID_STRING           HOSTNAME "_client"
#define  MQTT_CLIENT_STACK_SIZE     4096

#define  STRLEN(p)                  (sizeof(p) - 1)


/* Declare the MQTT thread stack space. */
static ULONG                        mqtt_client_stack[MQTT_CLIENT_STACK_SIZE / sizeof(ULONG)];

/* Declare the MQTT client control block. */
static NXD_MQTT_CLIENT              mqtt_client;

/* Define the symbol for signaling a received message. */


/* Define the test threads.  */
#define TOPIC_NAME                  "AZ3166"
#define MESSAGE_STARTUP             "Startup"
#define MESSAGE_BUTTON_A            "ButtonA"
#define MESSAGE_BUTTON_B            "ButtonB"



/* Define the priority of the MQTT internal thread. */
#define MQTT_THREAD_PRIORTY         2

/* Define the MQTT keep alive timer for 5 minutes */
#define MQTT_KEEP_ALIVE_TIMER       300

#define QOS0                        0
#define QOS1                        1

/* Declare event flag, which is used in this demo. */
TX_EVENT_FLAGS_GROUP                mqtt_app_flag;
#define DEMO_MESSAGE_EVENT          1
#define DEMO_ALL_EVENTS             3

/* Declare buffers to hold message and topic. */
static UCHAR message_buffer[NXD_MQTT_MAX_MESSAGE_LENGTH];
static UCHAR topic_buffer[NXD_MQTT_MAX_TOPIC_NAME_LENGTH];

/* Declare the disconnect notify function. */
static VOID disconnect_func(NXD_MQTT_CLIENT *client_ptr)
{
    NX_PARAMETER_NOT_USED(client_ptr);
    printf("client disconnected from server\n");
}

/*
static VOID notify_func(NXD_MQTT_CLIENT* client_ptr, UINT number_of_messages)
{
    NX_PARAMETER_NOT_USED(client_ptr);
    NX_PARAMETER_NOT_USED(number_of_messages);
    tx_event_flags_set(&mqtt_app_flag, DEMO_MESSAGE_EVENT, TX_OR);
    return;
  
}
*/

//void thread_mqtt_entry(NX_IP *ip_ptr, NX_PACKET_POOL *pool_ptr);
void mqtt_do(NX_IP *ip_ptr, NX_PACKET_POOL *pool_ptr);

static ULONG    error_counter;
// void thread_mqtt_entry(NX_IP *ip_ptr, NX_PACKET_POOL *pool_ptr)
void mqtt_do(NX_IP *ip_ptr, NX_PACKET_POOL *pool_ptr)
{
UINT status;
NXD_ADDRESS server_ip;
ULONG events;
UINT topic_length, message_length;

    printf("---> mqtt_do\r\n");

    /* Create MQTT client instance. */
    status = nxd_mqtt_client_create(&mqtt_client, "AZ3166", CLIENT_ID_STRING, STRLEN(CLIENT_ID_STRING),
                                    ip_ptr, pool_ptr, (VOID*)mqtt_client_stack, sizeof(mqtt_client_stack), 
                                    MQTT_THREAD_PRIORTY, NX_NULL, 0);
    
    if (status)
    {
        printf("Error in creating MQTT client: 0x%02x\n", status);
        error_counter++;
    }
    printf("    mqtt_do - mqtt client created\r\n");


#ifdef NXD_MQTT_OVER_WEBSOCKET
    status = nxd_mqtt_client_websocket_set(&mqtt_client, (UCHAR *)"test.mosquitto.org", sizeof("test.mosquitto.org") - 1,
                                           (UCHAR *)"/mqtt", sizeof("/mqtt") - 1);
    if (status)
    {
        printf("Error in setting MQTT over WebSocket: 0x%02x\r\n", status);
        error_counter++;
    }
#endif /* NXD_MQTT_OVER_WEBSOCKET */

    /* Register the disconnect notification function. */
    nxd_mqtt_client_disconnect_notify_set(&mqtt_client, disconnect_func);
    printf("    mqtt_do - nxd_mqtt_client_disconnect_notify_set done\r\n");
    
    /* Create an event flag for this demo. */
    //status = tx_event_flags_create(&mqtt_app_flag, "my app event");
    //if(status)
    //    error_counter++;
    

    server_ip.nxd_ip_version = 4;
    server_ip.nxd_ip_address.v4 = LOCAL_SERVER_ADDRESS;

    while (1) {

        while ( ! BUTTON_A_IS_PRESSED && ! BUTTON_B_IS_PRESSED ) 
            ;
    /* Start the connection to the server. */
    status = nxd_mqtt_client_connect(&mqtt_client, &server_ip, NXD_MQTT_PORT, 
                                     MQTT_KEEP_ALIVE_TIMER, 0, NX_WAIT_FOREVER);

    if(status) {
        error_counter++;
        printf("    mqtt_do - nxd_mqtt_client_connect error %02x\r\n",status);
    } else {
        printf("    mqtt_do - nxd_mqtt_client_connect done %02x\r\n",status);
    }


    /* Subscribe to the topic with QoS level 0. */
    
   /* status = nxd_mqtt_client_subscribe(&mqtt_client, TOPIC_NAME, STRLEN(TOPIC_NAME), QOS0);
    if(status) {
        error_counter++;
        printf("    mqtt_do - nxd_mqtt_client_subscribe error %02x\r\n",status);
    } else {
        printf("    mqtt_do - nxd_mqtt_client_subscribe done %02x\r\n",status);
    }   
    */

    /* Set the receive notify function. */
    
    /*
    status = nxd_mqtt_client_receive_notify_set(&mqtt_client, notify_func);
    if(status) {
        error_counter++;
        printf("    mqtt_do - nxd_mqtt_client_receive_notify_set error %02x\r\n",status);
    } else {
        printf("    mqtt_do - nxd_mqtt_client_receive_notify_set done %02x\r\n",status);
    }  
    */ 

    /* Publish a message with QoS Level 1. */
    /*status = nxd_mqtt_client_publish(&mqtt_client, TOPIC_NAME, STRLEN(TOPIC_NAME),
                                     (CHAR*)MESSAGE_STARTUP, STRLEN(MESSAGE_STARTUP), 0, QOS1, 1000 ); // NX_WAIT_FOREVER);

    printf("    mqtt_do - nxd_mqtt_client_publish done %02x\r\n",status);
*/
    /* Now wait for the broker to publish the message. */
    /*
    tx_event_flags_get(&mqtt_app_flag, DEMO_ALL_EVENTS, TX_OR_CLEAR, &events, TX_WAIT_FOREVER);
    if(events & DEMO_MESSAGE_EVENT)
    {
        status = nxd_mqtt_client_message_get(&mqtt_client, topic_buffer, sizeof(topic_buffer), &topic_length, 
                                             message_buffer, sizeof(message_buffer), &message_length);
        if(status == NXD_MQTT_SUCCESS)
        {
            topic_buffer[topic_length] = 0;
            message_buffer[message_length] = 0;
            printf("topic = %s, message = %s\n", topic_buffer, message_buffer);
        }
    }
    */

    // printf("work......\r\n");

    //while (1)
    //{
        if(BUTTON_A_IS_PRESSED) {
            printf("A ");
            status = nxd_mqtt_client_publish(&mqtt_client, TOPIC_NAME, STRLEN(TOPIC_NAME), (CHAR*)MESSAGE_BUTTON_A, STRLEN(MESSAGE_BUTTON_A), 0, QOS1, 10000 ); // NX_WAIT_FOREVER);
            printf("%0d\r\n", status);
        } else if(BUTTON_B_IS_PRESSED) {
            printf("B ");
            status = nxd_mqtt_client_publish(&mqtt_client, TOPIC_NAME, STRLEN(TOPIC_NAME), (CHAR*)MESSAGE_BUTTON_B, STRLEN(MESSAGE_BUTTON_B), 0, QOS1, 10000 ); // NX_WAIT_FOREVER);
            printf("%0d\r\n", status);
        }
    
        // status = nxd_mqtt_client_publish(&mqtt_client, TOPIC_NAME, STRLEN(TOPIC_NAME), (CHAR*)MESSAGE_BUTTON_B, STRLEN(MESSAGE_BUTTON_B), 0, QOS1, 1000 ); // NX_WAIT_FOREVER);
        // tx_thread_sleep(20000);



    /* Now unsubscribe the topic. */
    // nxd_mqtt_client_unsubscribe(&mqtt_client, TOPIC_NAME, STRLEN(TOPIC_NAME));

    /* Disconnect from the broker. */
    nxd_mqtt_client_disconnect(&mqtt_client);
    }

    /* Delete the client instance, release all the resources. */
    nxd_mqtt_client_delete(&mqtt_client);
    
    return;

}


#pragma GCC diagnostic pop