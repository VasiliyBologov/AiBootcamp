import asyncio
import os
import shutil
import subprocess
import time
from typing import Any

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse, MCPServerStdio
from agents.model_settings import ModelSettings

from get_env import load_env, get_env_value

load_env()
key = get_env_value('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = key

class DBAgent:
    def __init__(self):
        self.agent = None
        self.mcp = None

    async def run(self):
        self.mcp = MCPServerStdio(
            name="mongodb-mcp",
            params={
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "-e",
                    f"MDB_MCP_CONNECTION_STRING={get_env_value('MDB_MCP_CONNECTION_STRING')}",
                    "mongodb_mcp_server:latest"
                ]
            }
        )

        await self.mcp.connect()

        self.agent = Agent(
            name="Assistant",
            instructions="""Use the tools to find information in mongodb. Use 'giter_products' database and 'product' collection to find product. use only products where {'public': true}. Use scheam if you nedded `{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Goods",
  "type": "object",
  "properties": {
    "_id": { "type": "string" },
    "product_type": {
      "type": "string",
      "enum": [
        "fragrance", "makeup", "skincare", "candles", "diffusers", "health", "cosmetic_bag", "other"
      ]
    },
    "name": { "type": "string" },
    "brand_name": { "type": "string" },
    "name_from_brand": { "type": "string" },
    "description": {
      "$ref": "#/definitions/i18n"
    },
    "one_c_ode": { "type": "string" },
    "cover": {
      "$ref": "#/definitions/photo_for_goods"
    },
    "volume": {
      "$ref": "#/definitions/volume"
    },
    "public": { "type": "boolean" },
    "show": { "type": "boolean" },
    "prices": {
      "type": "object",
      "additionalProperties": { "$ref": "#/definitions/price" }
    },
    "goods_point": { "type": "number" },
    "update_date": { "type": "string", "format": "date-time" },
    "fragrance": { "$ref": "#/definitions/fragrance_fields" },
    "makeup": { "$ref": "#/definitions/makeup_fields" },
    "skincare": { "$ref": "#/definitions/skincare_fields" },
    "candle": { "$ref": "#/definitions/candle_fields" },
    "diffuser": { "$ref": "#/definitions/diffuser_fields" },
    "health": { "$ref": "#/definitions/health_fields" },
    "cosmetic_bag": { "$ref": "#/definitions/cosmetic_bag_fields" }
  },
  "required": ["product_type", "name", "update_date"],
  "definitions": {
    "i18n": {
      "type": "object",
      "properties": {
        "ru": { "type": "string" },
        "ro": { "type": "string" },
        "en": { "type": "string" },
        "ua": { "type": "string" },
        "it": { "type": "string" }
      },
      "additionalProperties": false
    },
    "photo_for_goods": {
      "type": "object",
      "properties": {
        "cover": { "type": "string" },
        "sampler": { "type": "string" },
        "additionalPics": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "volume": {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "unit": { "$ref": "#/definitions/i18n" }
      }
    },
    "price": {
      "type": "object",
      "properties": {
        "discount": {},
        "country": { "type": "string" },
        "price_client": { "type": "number" },
        "price_partner": { "type": "number" }
      }
    },
    "fragrance_fields": {
      "type": "object",
      "properties": {
        "collection_name": { "type": "string" },
        "sex": {
          "type": "string",
          "enum": ["man", "women", "unisex"]
        },
        "parfum_form": { "$ref": "#/definitions/i18n" },
        "fragrance_type": {
          "type": "array",
          "items": { "type": "string" }
        },
        "fragrance_number": { "type": "string" },
        "fragrance_top_notes": { "$ref": "#/definitions/i18n" },
        "fragrance_heart_notes": { "$ref": "#/definitions/i18n" },
        "fragrance_base_notes": { "$ref": "#/definitions/i18n" },
        "volume_variants": {
          "type": "object",
          "properties": {
            "3": { "type": "string" },
            "18": { "type": "string" },
            "50": { "type": "string" }
          }
        }
      }
    },
    "makeup_fields": {
      "type": "object",
      "properties": {
        "makeup_type": {
          "type": "string",
          "enum": [
            "mascara", "eyeliner", "lipGloss", "lipstick", "facePowder", "concealer", "highlighter"
          ]
        },
        "makeup_part": {
          "type": "string",
          "enum": ["face", "lips", "eyes"]
        },
        "color": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "color": { "type": "string" }
          }
        },
        "compound": { "$ref": "#/definitions/i18n" }
      }
    },
    "skincare_fields": {
      "type": "object",
      "properties": {
        "skin_care_place": {
          "type": "string",
          "enum": ["face", "body"]
        },
        "skin_care_sub_type": {
          "type": "string",
          "enum": ["care", "need"]
        },
        "skin_care_type": {
          "type": "array",
          "items": { "type": "string" }
        },
        "compound": { "$ref": "#/definitions/i18n" },
        "applying_method": { "$ref": "#/definitions/i18n" },
        "classification": { "type": "string" },
        "skin_type": { "type": "string" },
        "active_components": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "candle_fields": {
      "type": "object",
      "properties": {
        "candle_fragrance_type": { "$ref": "#/definitions/i18n" },
        "candle_compound": { "$ref": "#/definitions/i18n" }
      }
    },
    "diffuser_fields": {
      "type": "object",
      "properties": {
        "diffuser_fragrance_type": { "$ref": "#/definitions/i18n" },
        "diffuser_compound": { "$ref": "#/definitions/i18n" }
      }
    },
    "health_fields": {
      "type": "object",
      "properties": {
        "directions": { "$ref": "#/definitions/i18n" },
        "ingredients": { "$ref": "#/definitions/i18n" },
        "warnings": { "$ref": "#/definitions/i18n" },
        "storageConditions": { "$ref": "#/definitions/i18n" },
        "servingPerPackage": { "$ref": "#/definitions/i18n" }
      }
    },
    "cosmetic_bag_fields": {
      "type": "object",
      "properties": {
        "material": { "$ref": "#/definitions/i18n" },
        "size": { "$ref": "#/definitions/i18n" }
      }
    }
  }
}
`""",
            model="gpt-4.1-nano",
            mcp_servers=[self.mcp],
            # model_settings=ModelSettings(tool_choice="required"),
        )

    async def ask(self, message) -> str:
        trace_id = gen_trace_id()
        r = "No result"
        with trace(workflow_name="MCP ES", trace_id=trace_id):
            result = await Runner.run(starting_agent=self.agent, input=message)
            print(result.final_output)
            r = result.final_output
        return r

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mcp.exit_stack.pop_all()
